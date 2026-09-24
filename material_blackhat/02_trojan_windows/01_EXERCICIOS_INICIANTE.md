# Caderno de Exercícios Práticos: 02 Trojan Windows (Iniciante)

**Material de Referência:** `01_GUIA_PRATICO_INICIANTE.md`
**Script Base:** `keylogger_simples.py`

---

## 🎯 Objetivo Desta Lista

Praticar a lógica dos 4 módulos sem precisar de Windows com admin:
* Captura simulada com timestamp.
* Filtro de teclas e simulação de clipboard.
* Contadores e salvamento em log.
* Noção defensiva (o que o Blue Team veria).

---

## Exercício 1.1 — Mudando o Alvo para 10 Rodadas

### Enunciado
O script pede 5 linhas. Mude para 10 e teste com frases maiores.

### Tarefas
1. Altere `RODADAS = 5` para `10`.
2. Execute e digite senhas fracas de teste (`123456`, `senha123`).
3. Confirme que `log_simples.txt` tem 10 linhas (ou menos se digitou `sair`).

### Resolução Sugerida
```python
RODADAS = 10
ARQUIVO_LOG = "log_simples.txt"
```

---

## Exercício 1.2 — Contador de Caracteres Capturados

### Enunciado
Adicione `total_chars` que soma `len(texto)` a cada rodada e exibe no final.

### Tarefas
1. Crie `total_chars = 0` antes do loop.
2. Some `total_chars += len(texto)` por rodada.
3. Exiba `[*] Total de caracteres: X` ao final.

### Resolução Sugerida
```python
total_chars = 0
for i in range(1, RODADAS + 1):
    texto = input(f"[{i}/{RODADAS}] Digite algo (ou 'sair'): ")
    if texto.strip().lower() == "sair":
        break
    total_chars += len(texto)
    # ... grava no buf ...
print(f"[*] Total de caracteres capturados: {total_chars}")
```

---

## Exercício 1.3 — Filtrando Linha Vazia (como `if not senha: continue`)

### Enunciado
Se o usuário só apertar Enter, o script grava linha vazia. Pule essas linhas.

### Tarefas
1. Após o `input`, verifique `if not texto.strip(): continue` (antes do carimbo).
2. Teste apertando Enter 2x no meio da captura.

### Resolução Sugerida
```python
texto = input(f"[{i}/{RODADAS}] Digite algo (ou 'sair'): ")
if not texto.strip():
    print("[!] Linha vazia ignorada.")
    continue
```

---

## Exercício 1.4 — Gravando Janela Ativa Simulada

### Enunciado
O keylogger real grava `processo + janela` por tecla. Simule gravando `platform.node()` + nome digitado como "janela".

### Tarefas
1. Antes do loop, pergunte `janela = input("Nome da janela simulada (ex: notepad): ")`.
2. Grave `[HH:MM:SS] [janela] texto` em cada linha.
3. Abra `log_simples.txt` e confira o formato.

### Resolução Sugerida
```python
import platform
janela = input("Nome da janela simulada (ex: notepad): ").strip() or "simulada"
# dentro do loop:
buf.write(f"[{agora}] [{janela}@{platform.node()}] {texto}\n")
```
