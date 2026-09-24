# Exercícios: Burp no Brute Force

## Ex. 1 — Interceptar o Nível 01
Ative Intercept, rode `burp_proxy_config.py` 1 vez, encaminhe (Forward) e ache o JSON em history. **Esperado:** `{"usuario":"ana","senha":"..."}` + `401/200`.

## Ex. 2 — Intruder no Nível 02 (2 usuários)
Use pitchfork/cluster com `usuarios.txt` × `senhas.txt` (ou 2 rodadas Sniper). **Esperado:** `ana:123456` e `bruno:senha123` com `200`; `carlos` só `401`; `admin` dá `403` no `/login`.

## Ex. 3 — Rota admin (`/admin/login`)
Repita o Intruder contra `/admin/login` com `admin/admin123`. **Esperado:** agora `200` — prova de RBAC do guia 02.

## Ex. 4 — Repeater como debugger
Mande um JSON malformado (`{"usuario":"ana"}` sem senha) no Repeater. Anote o status (422/500?). **Discussão:** como Python trataria com `try/except` e como o servidor deveria validar?
