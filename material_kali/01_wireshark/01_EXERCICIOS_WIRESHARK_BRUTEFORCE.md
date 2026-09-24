# Exercícios: Wireshark no Brute Force

**Referência:** `01_GUIA_PRATICO_WIRESHARK_BRUTEFORCE.md` + `material_bruteforce/`

## Ex. 1 — Capture o Nível 01 e ache a senha no fio
1. Capture em `lo` (ou LAN) com `tcp port 8002`.
2. Rode `bruteforce_simples.py`.
3. Filtre `http.response.code == 200`, faça Follow Stream e anote `usuario/senha` vistos.
**Esperado:** 1 pacote `200` com `{"usuario":"ana","senha":"123456"}` visível.

## Ex. 2 — Conte 401 vs 200 no Nível 02 (multi-usuários)
1. Rode `bruteforce_multi_usuarios.py` capturando.
2. Use `tshark -r captura.pcap -Y http.response.code==401 | wc -l` e `...==200`.
3. Confira se o total bate com `total_requisicoes` do script.
**Esperado:** ex.: 4 usuários × até 5 senhas = contagem idêntica ao `print` do Python.

## Ex. 3 — Meça velocidade (req/s) no Wireshark
1. Rode `bruteforce_rockyou.py` com wordlist pequena.
2. Em Statistics → I/O Graph, plote `http.request` por segundo.
3. Compare com `Velocidade média: X req/s` do script.
**Esperado:** picos de N req/s + vales do `timeout=5`.

## Ex. 4 — Blue Team: escreva a regra
Com a captura aberta, responda: qual filtro detecta "5× `401` do mesmo IP em 10s"? Proponha bloqueio (rate-limit) + evidência (exporte `File → Export Specified Packets → Displayed`).
**Resposta modelo:** `http.response.code==401 && ip.src==<IP>` agrupado por 10s; após 5, RST/bloqueio temporário + log para SIEM.

## Ex. 5 — Prove o isolamento (Docker próprio + HTTP visível)
1. Suba seu lab: `cd banco_web && docker compose up --build`. Confirme `curl http://127.0.0.1:8002/api/saude`.
2. Capture com filtro `tcp.port == 8002` e rode `bruteforce_simples.py` contra `127.0.0.1`.
3. Em Conversations, confira que `ip.src` é só seu IP/`127.0.0.1` — nenhum pacote de colega aparece (rede chaveada não espelha unicast; loopback nem sai da máquina).
4. Faça Follow Stream no `200` e anote: senha em claro + `token` base64 + `Set-Cookie: nb_session`. Decodifique o token (`echo <token> | base64 -d`) e confira `usuario:papel:data`.
**Esperado:** só seu tráfego; senha + token + cookie legíveis porque é HTTP — contraste com o C2 HTTPS do guia 02.
