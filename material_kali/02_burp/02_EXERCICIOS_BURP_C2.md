# Exercícios: Burp no C2

## Ex. 1 — Provar o SSLError (sem CA)
Rode `git_trojan.py` com `HTTPS_PROXY` mas sem instalar a CA. **Esperado:** `SSLError: certificate verify failed` e nada no history — anote o erro.

## Ex. 2 — MITM com CA (com CA)
Instale a CA no `certifi`, rode 1 ciclo e decodifique `config/abc.json` no Decoder do Burp. **Esperado:** lista com `dirlister/environment/keylogger`.

## Ex. 3 — Editar resposta (Repeater/Match-Replace)
Crie regra para injetar `{ "module": "hostname" }` na resposta do `abc.json` e observe o trojan pedir módulo inexistente. **Esperado:** `[*] Attempting to retrieve hostname` + `ModuleNotFound` tratado — prova do poder do MITM em lab.

## Ex. 4 — Blue Team
Com o history cheio, responda: quais 2 headers (`User-Agent: github3.py`, `Authorization: token ***`) entregam o C2? Como rotacionar token + mudar UA dificultaria? (E por que ainda não basta — ver Wireshark comportamental.)
