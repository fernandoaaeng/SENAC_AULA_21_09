# Caderno de Exercícios Práticos: 01 GitHub C2 (Iniciante)

**Material de Referência:** `01_GUIA_PRATICO_INICIANTE.md`
**Script Base:** `github_c2_simples.py`
**Alvo:** Simulador local (`config_simulado.json` + `modulos_simples/`)

---

## 🎯 Objetivo Desta Lista

Praticar e fixar os conceitos fundamentais de C2 modular sem usar GitHub real:
* Leitura de lista de tarefas em JSON.
* Importação dinâmica com `importlib`.
* Execução em paralelo com `threading`.
* Salvamento de resultados com timestamp em arquivo.

---

## Exercício 1.1 — Adicionando um Novo Módulo na Lista

### Enunciado
O controlador quer executar uma terceira tarefa chamada `hostname_simples`, que apenas retorna o nome do computador.

### Tarefas
1. Crie o arquivo `modulos_simples/hostname_simples.py` com uma função `run()` que retorna o hostname.
2. Adicione `{ "module": "hostname_simples" }` ao `config_simulado.json`.
3. Execute `github_c2_simples.py` e confirme que 3 arquivos aparecem em `data_simulada/`.

### Resolução Sugerida
```python
# Arquivo: modulos_simples/hostname_simples.py
import socket

def run(**args):
    print("[*] In hostname_simples module.")
    return socket.gethostname()
```

```json
// Arquivo: config_simulado.json
[
  { "module": "dirlister_simples" },
  { "module": "environment_simples" },
  { "module": "hostname_simples" }
]
```

---

## Exercício 1.2 — Contador de Tarefas Executadas

### Enunciado
No script atual, não sabemos quantas tarefas foram concluídas.
Adicione uma variável contadora `concluidas` que soma `+1` a cada módulo finalizado.

### Tarefas
1. Crie `concluidas = 0` antes das threads (use `threading.Lock` para somar com segurança ou some após `join`).
2. Exiba `[Tarefa 1/2 concluída]` a cada salvamento.
3. Ao final, exiba o total.

### Resolução Sugerida
```python
import threading

concluidas = 0
cadeado = threading.Lock()

def executar_modulo(nome):
    global concluidas
    # ... importa e executa ...
    with cadeado:
        concluidas += 1
        print(f"[Tarefa {concluidas} concluída: {nome}]")
```

---

## Exercício 1.3 — Tratamento de Módulo Não Encontrado

### Enunciado
Se o JSON pedir um módulo que não existe na pasta, o script quebra com `ModuleNotFoundError`.
Implemente uma **flag de erro** para pular o módulo faltante e avisar no terminal.

### Tarefas
1. Envolva o `import_module` em `try/except ModuleNotFoundError`.
2. Quando falhar, imprima `[-] Módulo 'xxx' não encontrado. Pulando.` e não crie arquivo.
3. Teste adicionando `{ "module": "modulo_fantasma" }` ao JSON.

### Resolução Sugerida
```python
def executar_modulo(nome):
    try:
        modulo = importlib.import_module(f"{PASTA_MODULOS}.{nome}")
    except ModuleNotFoundError:
        print(f"[-] Módulo '{nome}' não encontrado. Pulando.")
        return
    resultado = modulo.run()
    # ... salva ...
```

---

## Exercício 1.4 — Gravando Relatório Consolidado (`relatorio_c2.txt`)

### Enunciado
Em auditorias, os resultados precisam ir para um relatório único, não só arquivos separados.
Modifique o script para, ao final de todas as threads, gerar `relatorio_c2.txt` com o resumo.

### Tarefas
1. Após o `join`, liste os arquivos criados em `data_simulada/`.
2. Grave `relatorio_c2.txt` com data, total de tarefas e nome de cada arquivo de resultado.

### Resolução Sugerida
```python
from pathlib import Path
from datetime import datetime

# após join das threads:
arquivos = sorted(Path(PASTA_RESULTADOS).glob("*.txt"))
with open("relatorio_c2.txt", "w", encoding="utf-8") as rel:
    rel.write(f"Relatório C2 simulado - {datetime.now().isoformat()}\n")
    rel.write(f"Total de resultados: {len(arquivos)}\n")
    for arq in arquivos:
        rel.write(f"- {arq.name}\n")

print("[+] Relatório gravado em 'relatorio_c2.txt'.")
```
