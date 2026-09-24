# Laboratório Prático: Trojan Modular, GitHub C2 e Tarefas no Windows

Bem-vindo ao material prático do módulo de **Comando e Controle (C2), Trojanização no Windows e Integração de Módulos com Python**.

Este ambiente foi estruturado em **três temas progressivos**, baseados em *Black Hat Python, 2ª Edição* (Cap. 7 e 8) + tutorial de integração. Cada tema é composto por **duas versões**:
1. **Versão Iniciante (simplificada):** Explicação com analogias, código curto sem dependências externas, execução 100% local e segura para sala de aula. *(Ideal para ler primeiro ou exportar em PDF)*.
2. **Versão Completa (fiel ao original):** Teoria integral, código real do livro, análise linha a linha e procedimento com GitHub + Windows. *(Para laboratório com supervisão do professor)*.

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> As técnicas deste material têm finalidade exclusiva de aprendizado de segurança defensiva e testes autorizados em ambiente de laboratório.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.
> Nunca suba token real para repositório público. Use sempre repositório **privado** e token de teste com validade curta.

---

## 🗺️ Mapa de Navegação e Arquivos

| Tema | Pasta | Guia Iniciante | Exercícios Iniciante | Script Iniciante | Guia Completo | Exercícios Completo | Scripts Completos | Foco do Aprendizado |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | `01_github_c2/` | `01_GUIA_PRATICO_INICIANTE.md` | `01_EXERCICIOS_INICIANTE.md` | `github_c2_simples.py` | `02_GUIA_PRATICO_COMPLETO.md` | `02_EXERCICIOS_COMPLETO.md` | `git_trojan.py`, `modules/dirlister.py`, `modules/environment.py`, `config/abc.json` | **C2 Modular:** config JSON, `import` dinâmico, `threading`, `GitImporter`, envio de resultados |
| **02** | `02_trojan_windows/` | `01_GUIA_PRATICO_INICIANTE.md` | `01_EXERCICIOS_INICIANTE.md` | `keylogger_simples.py` | `02_GUIA_PRATICO_COMPLETO.md` | `02_EXERCICIOS_COMPLETO.md` | `keylogger.py`, `screenshotter.py`, `shell_exec.py`, `sandbox_detect.py` | **Tarefas Windows:** keylogger, screenshot GDI, shellcode em memória, detecção de sandbox |
| **03** | `03_integracao_keylogger_github_trojan/` | `01_GUIA_PRATICO_INICIANTE.md` | `01_EXERCICIOS_INICIANTE.md` | `integracao_simples.py` | `02_GUIA_PRATICO_COMPLETO.md` | `02_EXERCICIOS_COMPLETO.md` | `modules/keylogger.py` (adaptado), `git_trojan_moderno.py`, `decodificar_resultado.py` | **Integração:** plugar keylogger no C2, `abc.json`, `find_spec`/`exec_module`, coleta com `base64 -d` |

---

## 🖨️ Dica: Como Salvar os Guias como PDF

Os arquivos Markdown (`.md`) foram diagramados com tabelas compactas, blocos de código com numeração de linha e espaçamentos planejados para impressão ou conversão em PDF:

* **No VS Code:** Instale a extensão **Markdown PDF** ou **Markdown Preview Enhanced**, clique com o botão direito no arquivo `.md` e escolha `Markdown PDF: Export (pdf)`.
* **No Navegador:** Abra o arquivo `.md` renderizado no GitHub/VS Code, pressione `Ctrl + P` (Imprimir) e selecione a opção **Salvar como PDF**.

> 💡 **Ordem de leitura sugerida:** `01_github_c2/01_GUIA_PRATICO_INICIANTE.md` → `02_trojan_windows/01_GUIA_PRATICO_INICIANTE.md` → `03_integracao.../01_GUIA_PRATICO_INICIANTE.md` → depois as versões `02_GUIA_PRATICO_COMPLETO.md` na mesma ordem.

---

## ⚙️ Pré-requisitos de Execução

**Para as versões INICIANTE (todas rodam em qualquer SO, sem GitHub):**
```bash
pip install requests
cd material_blackhat/01_github_c2
python github_c2_simples.py
```

**Para as versões COMPLETAS:**

Na máquina atacante (Kali/Linux):
```bash
pip install github3.py
```

Na máquina vítima de laboratório (Windows 10/11):
```cmd
pip install github3.py pyWinhook pywin32
```

* Token clássico do GitHub com escopo `repo` (nunca commitar o `mytoken.txt`).
* Repositório **privado** `bhtprojan` com pastas `config/`, `modules/`, `data/`.
* Python 3.6–3.11 para o código original do livro. Para Python 3.12+, use o `git_trojan_moderno.py` (com `find_spec`/`exec_module`).

---

## 📁 Estrutura Organizada dos Arquivos

```text
material_blackhat/
│
├── README.md                                <- Este índice geral
│
├── 01_github_c2/                            <- Cap. 7: GitHub como C2
│   ├── README.md
│   ├── 01_GUIA_PRATICO_INICIANTE.md         <- C2 com analogia de professor + pasta local
│   ├── 01_EXERCICIOS_INICIANTE.md           <- 4 exercícios com resolução
│   ├── github_c2_simples.py                 <- Simulador local sem GitHub (~40 linhas)
│   ├── config_simulado.json
│   ├── modulos_simples/dirlister_simples.py
│   ├── modulos_simples/environment_simples.py
│   ├── 02_GUIA_PRATICO_COMPLETO.md          <- Fiel ao black-hat-python-cap7-github-c2.md
│   ├── 02_EXERCICIOS_COMPLETO.md            <- Exercícios com threads, base64, GitImporter
│   ├── git_trojan.py                        <- Trojan original do livro
│   ├── config/abc.json
│   └── modules/dirlister.py
│   └── modules/environment.py
│
├── 02_trojan_windows/                       <- Cap. 8: Tarefas comuns no Windows
│   ├── README.md
│   ├── 01_GUIA_PRATICO_INICIANTE.md         <- O que é keylogger/screenshot/shellcode/sandbox
│   ├── 01_EXERCICIOS_INICIANTE.md           <- 4 exercícios seguros e multiplataforma
│   ├── keylogger_simples.py                 <- Simulador via input() + log com timestamp
│   ├── 02_GUIA_PRATICO_COMPLETO.md          <- Fiel ao black-hat-python-cap8-trojaning-windows.md
│   ├── 02_EXERCICIOS_COMPLETO.md            <- Exercícios de TIMEOUT, GDI, VirtualAlloc, GetAsyncKeyState
│   ├── keylogger.py
│   ├── screenshotter.py
│   ├── shell_exec.py
│   └── sandbox_detect.py
│
└── 03_integracao_keylogger_github_trojan/    <- Integração Cap. 7 + Cap. 8
    ├── README.md
    ├── 01_GUIA_PRATICO_INICIANTE.md         <- Arquitetura atacante/GitHub/vítima simplificada
    ├── 01_EXERCICIOS_INICIANTE.md           <- 4 exercícios de integração local
    ├── integracao_simples.py                <- Simula push/pull sem GitHub real
    ├── 02_GUIA_PRATICO_COMPLETO.md          <- Fiel ao tutorial-integracao-keylogger-github-trojan.md
    ├── 02_EXERCICIOS_COMPLETO.md            <- Exercícios de token, abc.json, troubleshooting, OPSEC
    ├── modules/keylogger.py                 <- Versão adaptada (run(**args) + time.time())
    ├── git_trojan_moderno.py                <- GitImporter com find_spec/exec_module (Py 3.12+)
    └── decodificar_resultado.py             <- Decodifica .data de base64 para texto
```

---

## 🧭 De onde veio cada arquivo completo?

| Arquivo completo neste material | Arquivo original na raiz |
| :--- | :--- |
| `01_github_c2/02_GUIA_PRATICO_COMPLETO.md` | `black-hat-python-cap7-github-c2.md` |
| `02_trojan_windows/02_GUIA_PRATICO_COMPLETO.md` | `black-hat-python-cap8-trojaning-windows.md` |
| `03_integracao_keylogger_github_trojan/02_GUIA_PRATICO_COMPLETO.md` | `tutorial-integracao-keylogger-github-trojan.md.md` |

As versões `02_GUIA_PRATICO_COMPLETO.md` preservam todo o conteúdo técnico original, apenas reformatadas no padrão deste curso (cabeçalho de laboratório, tabelas Linha/Código/Finalidade, procedimento de execução e saída esperada).
