# Módulo 03 — Integração: Keylogger dentro do GitHub C2

**Tema:** Tutorial de integração Cap. 7 + Cap. 8
**Pasta:** `material_blackhat/03_integracao_keylogger_github_trojan/`

---

## 📖 O que tem nesta pasta?

| Versão | Guia | Exercícios | Scripts | Para quem? |
| :--- | :--- | :--- | :--- | :--- |
| **Iniciante** | `01_GUIA_PRATICO_INICIANTE.md` | `01_EXERCICIOS_INICIANTE.md` | `integracao_simples.py` | Entende o fluxo atacante → GitHub → vítima sem GitHub real (simula `push`/`pull` com pastas locais). |
| **Completa** | `02_GUIA_PRATICO_COMPLETO.md` | `02_EXERCICIOS_COMPLETO.md` | `modules/keylogger.py`, `git_trojan_moderno.py`, `decodificar_resultado.py` | Executa a integração real: token, `abc.json` com 3 módulos, `find_spec`/`exec_module` (Py 3.12+) e coleta com `base64 -d`. |

---

## 🧭 Ordem sugerida

1. Leia `01_GUIA_PRATICO_INICIANTE.md` e rode `python integracao_simples.py`.
2. Faça `01_EXERCICIOS_INICIANTE.md`.
3. Só então leia `02_GUIA_PRATICO_COMPLETO.md` (fiel ao `tutorial-integracao-keylogger-github-trojan.md.md`) com repositório **privado**.
4. Faça `02_EXERCICIOS_COMPLETO.md` (token, troubleshooting, OPSEC).

> ⚠️ A versão completa exige: conta GitHub de laboratório, repo privado `bhtprojan`, token clássico `repo` e VM Windows para o keylogger real. Nunca exponha `mytoken.txt`.
