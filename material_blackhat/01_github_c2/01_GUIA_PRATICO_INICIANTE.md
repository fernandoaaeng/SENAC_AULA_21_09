# Guia Prático Iniciante: GitHub como Comando e Controle (C2)

**Laboratório Prático:** BHT Lab Local (simulação sem GitHub real)
**Ambiente de Testes:** Python 3 + Biblioteca padrão (`json`, `threading`, `time`)
**Código de Apoio:** `github_c2_simples.py`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> As técnicas demonstradas neste material têm como finalidade exclusiva o aprendizado de segurança defensiva e testes autorizados em ambiente de laboratório.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. A Analogia: Professor, Lista de Tarefas e Alunos

Imagine uma sala de aula sem chamada oral:

```text
+-----------------------+                    +-----------------------+
|   CONTROLADOR (GitHub)|                    |   AGENTE (Trojan)     |
|                       |  1. LISTA          |                       |
|  Professor escreve    | -----------------> |  Aluno lê a lista     |
|  config.json com      |  quais módulos     |  e executa cada       |
|  tarefas do dia       |  executar          |  tarefa em paralelo   |
|                       |  2. ENTREGA        |                       |
|  Recebe os trabalhos  | <----------------- |  Devolve resultados   |
|  na pasta data/       |  arquivos .data    |  para a pasta data/   |
+-----------------------+                    +-----------------------+
```

1. **Controlador:** É quem decide *o que* será executado. No livro é um repositório GitHub. Aqui no iniciante é um simples arquivo `config_simulado.json` na sua pasta.
2. **Agente:** É o programa na máquina auditada. Ele lê a lista, executa cada módulo e devolve o resultado.
3. **Módulo:** É cada tarefinha separada (ex.: listar arquivos, ver variáveis de ambiente). Todo módulo tem a mesma porta de entrada: uma função chamada `run()`.

> 💡 **A lógica central do C2 modular:**
> O agente não sabe de antemão o que vai fazer. A cada ciclo ele pergunta ao controlador "o que executo agora?", recebe uma lista JSON, importa os módulos dinamicamente e envia os resultados de volta. Para trocar o comportamento, basta editar o JSON — sem reinstalar o agente.

---

## 2. Estrutura de uma Tarefa (config JSON)

Para conversar com o agente, o controlador escreve um **arquivo de configuração JSON**. Essa mensagem tem formato de lista:

```json
[
  { "module": "dirlister_simples" },
  { "module": "environment_simples" }
]
```

* **Lista `[...]GP:** Permite pedir 1, 2 ou 10 módulos de uma vez.
* **Chave `"module"`:** É o nome do arquivo Python (sem `.py`) que está na pasta `modulos_simples/`.
* **Para adicionar uma tarefa nova:** Basta acrescentar um bloco `{ "module": "nome_novo" }`.

---

## 3. Conceitos de Python Utilizados no Código

O script `github_c2_simples.py` foi construído de forma linear, utilizando apenas 5 comandos fundamentais:

### A. Variáveis de Configuração
Guardam os parâmetros no topo para fácil edição:
```python
ARQUIVO_CONFIG = "config_simulado.json"
PASTA_MODULOS = "modulos_simples"
PASTA_RESULTADOS = "data_simulada"
```

### B. Leitura de JSON com `json.load()`
O JSON é o "idioma" entre controlador e agente:
```python
with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
    tarefas = json.load(f)  # vira lista Python: [{"module": ...}, ...]
```

### C. Importação Dinâmica com `importlib`
Em vez de `import fixo` no topo, o agente importa pelo **nome que veio do JSON**:
```python
modulo = importlib.import_module(f"modulos_simples.{nome}")
resultado = modulo.run()
```
* Isso é a versão simplificada do `GitImporter` do livro (que baixa da internet; aqui lê da pasta local).

### D. Execução em Paralelo com `threading.Thread`
Cada módulo roda numa thread para não travar os outros:
```python
thread = threading.Thread(target=executar_modulo, args=(nome,))
thread.start()
```

### E. Salvamento de Resultado com `open(..., "w")`
Cada resultado vira um arquivo com data e hora, igual ao `data/<id>/<timestamp>.data` do GitHub:
```python
with open(caminho_saida, "w", encoding="utf-8") as saida:
    saida.write(str(resultado))
```

---

## 4. Análise Linha a Linha do Código

```python
 1 | import json
 2 | import threading
 3 | import time
 4 | from datetime import datetime
 5 | from pathlib import Path
 6 | import importlib
 7 |
 8 | # 1. Parâmetros de configuração
 9 | ARQUIVO_CONFIG = "config_simulado.json"
10 | PASTA_MODULOS = "modulos_simples"
11 | PASTA_RESULTADOS = "data_simulada"
12 |
13 | print("=" * 60)
14 | print("   SIMULADOR LOCAL DE C2 (sem GitHub)")
15 | print("=" * 60)
16 |
17 | # 2. Leitura da lista de tarefas
18 | with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
19 |     tarefas = json.load(f)
20 |
21 | print(f"[+] Tarefas recebidas: {[t['module'] for t in tarefas]}")
22 |
23 | # 3. Função que executa um módulo isolado
24 | def executar_modulo(nome):
25 |     print(f"[*] Executando módulo: {nome}")
26 |     modulo = importlib.import_module(f"{PASTA_MODULOS}.{nome}")
27 |     resultado = modulo.run()
28 |     carimbo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
29 |     destino = Path(PASTA_RESULTADOS) / f"{nome}_{carimbo}.txt"
30 |     destino.parent.mkdir(parents=True, exist_ok=True)
31 |     destino.write_text(str(resultado), encoding="utf-8")
32 |     print(f"[+] Resultado de '{nome}' salvo em: {destino}")
33 |
34 | # 4. Disparo em paralelo + espera
35 | threads = []
36 | for tarefa in tarefas:
37 |     th = threading.Thread(target=executar_modulo, args=(tarefa["module"],))
38 |     th.start()
39 |     threads.append(th)
40 |     time.sleep(1)
41 |
42 | for th in threads:
43 |     th.join()
44 |
45 | print("Ciclo concluído. Verifique a pasta data_simulada/")
```

| Linhas | Instrução | Finalidade Técnica |
| :---: | :--- | :--- |
| `1–6` | `import ...` | Carrega JSON, threads, tempo e importação dinâmica. |
| `9–11` | Definição de variáveis | Armazena nomes de arquivo e pastas do laboratório local. |
| `18–19` | `json.load(f)` | Converte o JSON do controlador em lista Python. |
| `24–32` | `def executar_modulo(nome):` | Importa o módulo pelo nome, chama `run()` e salva o retorno. |
| `26` | `importlib.import_module(...)` | Versão local e segura do `GitImporter` (sem rede). |
| `28–31` | `datetime + Path.write_text` | Cria arquivo de resultado com timestamp, como o `.data` do GitHub. |
| `37–38` | `threading.Thread(...).start()` | Executa cada módulo em paralelo. |
| `42–43` | `th.join()` | Aguarda todas as threads terminarem antes de encerrar. |

---

## 5. Procedimento de Execução no Terminal

1. Certifique-se de que a estrutura existe:
   ```text
   config_simulado.json
   modulos_simples/dirlister_simples.py
   modulos_simples/environment_simples.py
   github_c2_simples.py
   ```
2. Conteúdo do `config_simulado.json`:
   ```json
   [
     { "module": "dirlister_simples" },
     { "module": "environment_simples" }
   ]
   ```
3. Execute o simulador:
   ```bash
   python github_c2_simples.py
   ```
4. **Saída esperada:**
   ```text
   ============================================================
      SIMULADOR LOCAL DE C2 (sem GitHub)
   ============================================================
   [+] Tarefas recebidas: ['dirlister_simples', 'environment_simples']
   [*] Executando módulo: dirlister_simples
   [*] Executando módulo: environment_simples
   [+] Resultado de 'dirlister_simples' salvo em: data_simulada/dirlister_simples_20260924_013000_123456.txt
   [+] Resultado de 'environment_simples' salvo em: data_simulada/environment_simples_20260924_013001_654321.txt
   Ciclo concluído. Verifique a pasta data_simulada/
   ```

> 📌 **Ponte para a versão completa:**
> No Cap. 7 real, o `config_simulado.json` vira `config/abc.json` no GitHub, o `importlib.import_module` vira o `GitImporter` (que baixa `.py` da internet via `github3.py`), e a pasta `data_simulada/` vira `data/abc/*.data` no repositório. A lógica é idêntica — só muda o transporte.
