# Guia Prático Iniciante: O que um Trojan Faz no Windows?

**Laboratório Prático:** BHT Lab Local (simulação multiplataforma, sem admin)
**Ambiente de Testes:** Python 3 puro (sem `pyWinhook`/`pywin32`)
**Código de Apoio:** `keylogger_simples.py`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> As técnicas demonstradas neste material têm como finalidade exclusiva o aprendizado de segurança defensiva e testes autorizados em ambiente de laboratório.
> Hooks reais de teclado exigem privilégio de administrador e só devem ser testados em VM de laboratório.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. Os 4 Poderes do Trojan (Analogia dos 4 Espiões)

Quando o trojan chega na máquina Windows, ele pode plugar 4 "espiões", cada um com uma função:

```text
+-----------------------+                    +-----------------------+
|   VÍTIMA (Windows)    |                    |   ESPIÕES (módulos)   |
|                       |  TECLAS            |  keylogger: anota     |
|  Usuário digita       | -----------------> |  tudo + Ctrl+V        |
|  senha no notepad     |  TELA              |  screenshot: foto     |
|  Abre calculadora     | -----------------> |  da tela via GDI      |
|  Nada suspeito        |  MEMÓRIA           |  shell_exec: executa  |
|  roda em VM           | -----------------> |  código sem disco     |
|  Antivírus observa    |  FUGA              |  sandbox_detect:      |
|                       | -----------------> |  percebe VM e se cala |
+-----------------------+                    +-----------------------+
```

1. **Keylogger:** Anota teclas + clipboard em `Ctrl+V`. Porta de entrada: `run()` que devolve string de log.
2. **Screenshot:** Fotografa a tela via GDI e salva `.bmp`.
3. **Shellcode:** Baixa código em base64, coloca em memória RWX (`VirtualAlloc`) e executa sem tocar o disco.
4. **Sandbox:** Conta teclas/cliques e tempo sem input. Se parecer robô, se encerra (`sys.exit(0)`) para não ser analisado.

> 💡 **A lógica central:**
> Todos expõem (ou são adaptados para) `run()`. O C2 do módulo 01 não precisa saber detalhes de Windows — só chama `run()` e recebe string/bytes de volta.

---

## 2. Como Simulamos sem Ser Admin?

Um hook real (`pyHook.HookManager + PumpWaitingMessages`) intercepta **todo** o teclado do Windows. Isso exige admin e só roda no Windows.

Para aprender a lógica sem risco, o `keylogger_simples.py` troca o hook por `input()`:

* **Real:** `hm.KeyDown = callback` + loop de mensagens COM por 10 min.
* **Simples:** `input("Digite (ou 'sair'): ")` em loop por N rodadas + `datetime.now()` + captura simulada de "janela ativa" via `platform.node()`.

O restante é idêntico: redireciona saída para `StringIO`, carimba hora, salva `log_simples.txt` e devolve string — igual ao `return log` do original.

---

## 3. Conceitos de Python Utilizados no Código

### A. Variáveis de Configuração
```python
RODADAS = 5
ARQUIVO_LOG = "log_simples.txt"
```

### B. Buffer em Memória com `StringIO`
Guarda tudo que seria `print()` e devolve de uma vez:
```python
from io import StringIO
buf = StringIO()
buf.write("ola")
log = buf.getvalue()  # "ola"
```

### C. Carimbo de Hora com `datetime`
Cada linha ganha `[HH:MM:SS]` para auditoria, igual ao `.data` do GitHub:
```python
from datetime import datetime
agora = datetime.now().strftime("%H:%M:%S")
```

### D. Loop Controlado por Contador (em vez de `TIMEOUT`)
No original é `while time < TIMEOUT`. Aqui é `for i in range(RODADAS)` — previsível para sala de aula.

---

## 4. Análise Linha a Linha do Código

```python
 1 | from datetime import datetime
 2 | from io import StringIO
 3 | import platform
 4 |
 5 | # 1. Parâmetros de configuração
 6 | RODADAS = 5
 7 | ARQUIVO_LOG = "log_simples.txt"
 8 |
 9 | print("=" * 60)
10 | print("   KEYLOGGER SIMULADO (sem hook, via input)")
11 | print("=" * 60)
12 |
13 | # 2. Prepara buffer em memória
14 | buf = StringIO()
15 | buf.write(f"[INFO] Maquina: {platform.node()} | Sistema: {platform.system()}\n")
16 |
17 | # 3. Loop de captura simulada
18 | for i in range(1, RODADAS + 1):
19 |     texto = input(f"[{i}/{RODADAS}] Digite algo (ou 'sair'): ")
20 |     if texto.strip().lower() == "sair":
21 |         break
22 |     agora = datetime.now().strftime("%H:%M:%S")
23 |     if texto.startswith("[PASTE]"):
24 |         buf.write(f"[{agora}] [PASTE] - {texto[7:]}\n")
25 |     else:
26 |         buf.write(f"[{agora}] {texto}\n")
27 |
28 | # 4. Salva e devolve o log
29 | log = buf.getvalue()
30 | with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
31 |     f.write(log)
32 |
33 | print("=" * 60)
34 | print(log)
35 | print(f"[+] Log salvo em '{ARQUIVO_LOG}'.")
```

| Linhas | Instrução | Finalidade Técnica |
| :---: | :--- | :--- |
| `1–3` | `import ...` | Hora, buffer e info da máquina. |
| `6–7` | Configurações | Nº de rodadas e nome do log. |
| `14–15` | `StringIO() + write` | Inicia buffer com cabeçalho da máquina. |
| `18` | `for i in range(...)` | Versão didática do `while < TIMEOUT`. |
| `19` | `input(...)` | Substitui o hook de teclado (seguro e multiplataforma). |
| `22` | `datetime.now().strftime` | Carimba cada linha, como auditoria Blue Team. |
| `23–26` | `if [PASTE]` | Simula a captura de clipboard do `Ctrl+V` real. |
| `29–31` | `getvalue + open(w)` | Recupera log e salva em disco. |

---

## 5. Procedimento de Execução no Terminal

1. Execute em qualquer SO:
   ```bash
   python keylogger_simples.py
   ```
2. Digite 5 linhas (tente `[PASTE]senha123` em uma delas) ou `sair` para encerrar antes.
3. **Saída esperada:**
   ```text
   ============================================================
      KEYLOGGER SIMULADO (sem hook, via input)
   ============================================================
   [1/5] Digite algo (ou 'sair'): ola mundo
   [2/5] Digite algo (ou 'sair'): [PASTE]senha123
   [3/5] Digite algo (ou 'sair'): sair
   ============================================================
   [INFO] Maquina: LAB-PC01 | Sistema: Windows
   [10:31:11] ola mundo
   [10:31:15] [PASTE] - senha123

   [+] Log salvo em 'log_simples.txt'.
   ```

> 📌 **Ponte para a versão completa:**
> No Cap. 8 real, o `input()` vira `pyHook.HookManager + PumpWaitingMessages`, o `platform.node()` vira `GetForegroundWindow + GetModuleBaseNameA`, e o `[PASTE]` vira `win32clipboard.GetClipboardData()`. O `run()` continua devolvendo string — por isso pluga direto no C2.
