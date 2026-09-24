# Exercícios: Hydra vs Python

## Ex. 1 — Mesmo alvo, dois ataques (Nível 01)
1. Rode `time python bruteforce_simples.py` e anote tempo + tentativas.
2. Rode `time hydra -l ana -P senhas.txt 127.0.0.1 -s 8002 http-post-form "/login:usuario=^USER^&senha=^PASS^:F=401" -t 4` (adapte se o lab exige JSON — ver guia §3).
3. **Esperado:** ambos acham `123456`; Hydra costuma ser mais rápido com `-t`; Python explica cada `status_code`.

## Ex. 2 — Hydra no Nível 02 + relatório Python
Rode Hydra com `-L usuarios.txt -P senhas.txt` e depois o script que gera `contas_comprometidas.csv`. **Pergunta:** qual saída o Blue Team prefere como evidência? (Resposta: CSV + `auditoria.log` do Python.)

## Ex. 3 — Rockyou pequeno (Nível 03)
Crie `mini_rockyou.txt` com 20 linhas e a senha no fim. Compare `time` dos dois + `req/s` do Wireshark. **Esperado:** Hydra escala com `-t 16`; Python escala reescrevendo com `ThreadPool`.

## Ex. 4 — Quando Hydra perde
Force JSON puro (sem fallback form) e mostre Hydra recebendo `422` em tudo enquanto `bruteforce_rockyou.py` acha com `200`. Escreva 3 linhas: por que automação própria vence ferramenta genérica aqui? (Resposta: controle de `json=`, `timeout`, `try/except`, `latin-1`.)
