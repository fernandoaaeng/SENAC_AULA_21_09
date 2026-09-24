# Exercícios: Hydra no Cenário C2 (limites)

## Ex. 1 — Kill-chain completo (lab)
1. Use Hydra para achar `admin:admin123` em `/admin/login`.
2. "Com a senha", implante `git_trojan.py` (simulado) e rode 1 ciclo.
**Esperado:** Hydra abre a porta; C2 mantém o acesso — fases distintas.

## Ex. 2 — Entropia do token
Tente `hydra -l x -P rockyou.txt api.github.com ...` (NÃO vai achar; cancele com `Ctrl+C`). Calcule: 40 chars base62 = 62^40 tentativas. **Resposta:** força bruta em token é inviável — por isso roubam/vazam, não quebram.

## Ex. 3 — Wireshark comparativo
Capture Hydra (`rajada form`) vs trojan (`burst TLS espaçado`). **Esperado:** Hydra é barulhento e rápido; C2 é silencioso e lento — EDRs diferentes para cada.

## Ex. 4 — Redação Blue Team (5 linhas)
Se você visse Hydra + depois beacon GitHub do mesmo IP, qual playbook? (Resposta: isolar host, revogar token, auditar `create_file`, girar credenciais `/admin`.)
