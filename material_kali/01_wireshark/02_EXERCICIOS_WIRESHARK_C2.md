# Exercícios: Wireshark no C2

## Ex. 1 — Controle negativo (simulador local)
Rode `github_c2_simples.py` capturando `host api.github.com`. **Esperado:** zero pacotes — prova que simulador não vaza para internet.

## Ex. 2 — Beacon real (lab com token de teste)
Capture 2 ciclos de `git_trojan.py` (use sleep curto temporário de 60s para aula). Meça intervalo e bytes por ciclo em Conversations. **Esperado:** 2 bursts parecidos, intervalos irregulares.

## Ex. 3 — SNI como IOC
Filtre `tls.handshake.extensions_server_name contains "github"` e exporte os ClientHello. Responda: como um proxy com allowlist bloquearia este C2 sem quebrar devs? (Resposta: allowlist por grupo + exceção só para grupo dev + alerta em estação comum).

## Ex. 4 — Comparar brute vs C2 no fio
Abra lado a lado `captura_brute.pcap` (HTTP claro) e `captura_c2.pcap` (TLS). Escreva 3 linhas: por que brute se detecta por assinatura e C2 por comportamento?
