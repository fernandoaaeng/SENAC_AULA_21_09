# Módulo 02 — Tarefas Comuns de Trojan no Windows

**Tema:** Cap. 8 do *Black Hat Python* (Windows-only)
**Pasta:** `material_blackhat/02_trojan_windows/`

---

## 📖 O que tem nesta pasta?

| Versão | Guia | Exercícios | Scripts | Para quem? |
| :--- | :--- | :--- | :--- | :--- |
| **Iniciante** | `01_GUIA_PRATICO_INICIANTE.md` | `01_EXERCICIOS_INICIANTE.md` | `keylogger_simples.py` | Explica os 4 módulos com analogias e roda um keylogger simulado multiplataforma (via `input()`, sem hook de admin). |
| **Completa** | `02_GUIA_PRATICO_COMPLETO.md` | `02_EXERCICIOS_COMPLETO.md` | `keylogger.py`, `screenshotter.py`, `shell_exec.py`, `sandbox_detect.py` | Código real do livro para VM Windows de laboratório (`pyWinhook`, `pywin32`, `ctypes`). |

---

## 🧭 Ordem sugerida

1. Leia `01_GUIA_PRATICO_INICIANTE.md` e rode `python keylogger_simples.py` em qualquer SO.
2. Faça `01_EXERCICIOS_INICIANTE.md`.
3. Só então leia `02_GUIA_PRATICO_COMPLETO.md` (fiel ao `black-hat-python-cap8-trojaning-windows.md`) em VM Windows com supervisão.
4. Faça `02_EXERCICIOS_COMPLETO.md`.

> ⚠️ Os 4 scripts completos são **Windows-only** e exigem privilégio de administrador para hooks. Use apenas VM de laboratório. O `shell_exec.py` baixa e executa shellcode em memória — manuseie apenas o exemplo inofensivo (`calc.exe`) do professor.
