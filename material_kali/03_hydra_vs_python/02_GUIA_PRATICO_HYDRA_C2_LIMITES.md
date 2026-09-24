# Guia Prático: Por que Hydra NÃO Substitui o C2 GitHub

**Laboratório:** `bhtprojan` (GitHub API + token + base64 + módulos)
**Ideia:** mostrar o limite da ferramenta pronta — e quando Python é obrigatório.

## 1. O que Hydra sabe fazer (e o C2 não é)
Hydra faz **tentativas de login** (`user×pass → 200/401`). O C2 faz **pós-acesso modular** (baixa `.py`, executa `run()`, envia `.data`). São fases diferentes do ataque.

```text
[Hydra] --mil logins--> [/login] --acha senha--> [fim]
[Trojan] --1 token válido--> [GET abc.json] --> [GET keylogger.py] --> [POST .data] (loop 30m-3h)
```

## 2. Tentativa honesta (e por que falha)
```bash
# NÃO funciona: GitHub exige Authorization + JSON + base64, não form:
hydra -l x -P senhas.txt api.github.com -s 443 https-post-form "/repos/u/bhtprojan:F=404" -t 1
```
Hydra não monta `Authorization: token ghp_...`, não decodifica base64, não executa `GitImporter`. O trojan precisa de **lógica**, não de força bruta.

## 3. Onde Hydra AJUDA no cenário C2 (lab honesto)
* Força bruta no `/admin/login` **antes** do C2 (achar `admin:admin123` para então instalar o trojan) — aí vale o comparativo do guia 01.
* Auditar token fraco? Não — token tem 40 chars aleatórios, wordlist não acha. Aula de entropia.

| Tarefa | Hydra | Python trojan |
| :--- | :--- | :--- |
| Achar senha fraca `/login` | ✅ ideal | ✅ didático |
| Falar GitHub API com token | ❌ | ✅ (`github3.py`) |
| Import dinâmico + threads | ❌ | ✅ |
| Beacon 30m–3h | ❌ | ✅ |

> Conclusão: Hydra é **pré-acesso**; trojan é **pós-acesso**. Usar os dois na mesma aula mostra o kill-chain completo.
