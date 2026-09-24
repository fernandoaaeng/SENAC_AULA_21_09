# Caderno de Exercícios Práticos: 03 Integração (Iniciante)

**Material de Referência:** `01_GUIA_PRATICO_INICIANTE.md`
**Script Base:** `integracao_simples.py`

---

## 🎯 Objetivo Desta Lista

Praticar o fluxo completo sem GitHub real:
* Publicar config com 3 módulos.
* Simular import dinâmico e coleta.
* Tratar módulo faltante e log vazio.
* Gerar relatório final da integração.

---

## Exercício 1.1 — Publicando Só o Keylogger

### Enunciado
Mude o `push` para publicar apenas `[{ "module": "keylogger_simples" }]` e observe que só 1 resultado aparece.

### Tarefas
1. Edite a variável `config` no script.
2. Apague `github_simulado/data/abc/*.txt` e rode de novo.
3. Confirme que só 1 `.txt` foi criado.

### Resolução Sugerida
```python
config = [{"module": "keylogger_simples"}]
(BASE / "config" / "abc.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
```

---

## Exercício 1.2 — Contador de Resultados Coletados

### Enunciado
Adicione `coletados = 0` e some `+1` por módulo com resultado não-vazio.

### Tarefas
1. Inicialize antes do `for`.
2. Após `resultado = mod.run()`, verifique `if str(resultado).strip(): coletados += 1`.
3. Exiba `[*] Resultados válidos: X/Y`.

### Resolução Sugerida
```python
coletados = 0
for t in tarefas:
    resultado = mod.run()
    if str(resultado).strip():
        coletados += 1
print(f"[*] Resultados válidos: {coletados}/{len(tarefas)}")
```

---

## Exercício 1.3 — Pulando Módulo Fantasma sem Quebrar

### Enunciado
Adicione `{ "module": "modulo_fantasma" }` ao push e trate `ModuleNotFoundError` no pull.

### Tarefas
1. Inclua o fantasma na lista publicada.
2. Envolva `import_module` em `try/except`.
3. Confirme que os 3 reais executam e o fantasma só loga `[-] não encontrado`.

### Resolução Sugerida
```python
try:
    mod = importlib.import_module(f"github_simulado.modules.{nome}")
except ModuleNotFoundError:
    print(f"[-] Módulo '{nome}' não encontrado. Pulando.")
    continue
```

---

## Exercício 1.4 — Relatório `relatorio_integracao.txt`

### Enunciado
Gere um relatório único listando cada `.txt` em `data/abc/` com tamanho em bytes.

### Tarefas
1. Após o loop, liste `sorted((BASE/"data"/"abc").glob("*.txt"))`.
2. Grave `relatorio_integracao.txt` com data + `nome - N bytes` por linha.

### Resolução Sugerida
```python
arquivos = sorted((BASE / "data" / "abc").glob("*.txt"))
with open("relatorio_integracao.txt", "w", encoding="utf-8") as rel:
    rel.write(f"Integração simulada - {datetime.now().isoformat()}\n")
    for arq in arquivos:
        rel.write(f"- {arq.name} - {arq.stat().st_size} bytes\n")
print("[+] Relatório gravado em 'relatorio_integracao.txt'.")
```
