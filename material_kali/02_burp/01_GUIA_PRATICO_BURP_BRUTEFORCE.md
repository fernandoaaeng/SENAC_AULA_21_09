# Guia Prático: Burp Suite no Brute Force

**Laboratório:** NexusBank `/login` + `/admin/login`
**Ferramenta:** Burp Suite Community → Proxy + Repeater + Intruder
**Apoio:** `burp_proxy_config.py`

## 1. Arquitetura (Burp no meio)

```text
[Script Python] --proxies 127.0.0.1:8080--> [Burp Proxy] --forward--> [NexusBank:8002]
     requests.post(url, json=..., proxies=proxies, verify=False)
```

## 2. Setup (5 min)
1. Kali: `burpsuite &` → Proxy → Intercept **off** inicialmente → Options: listener `127.0.0.1:8080` ativo.
2. No script de aula, use:
   ```python
   import requests, urllib3
   urllib3.disable_warnings()
   proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
   r = requests.post("http://127.0.0.1:8002/login", json={"usuario": "ana", "senha": "123456"}, proxies=proxies, verify=False)
   ```
   (Ver arquivo `burp_proxy_config.py` pronto.)
3. Rode 1 vez e veja o POST aparecer em **HTTP history**.

## 3. Repeater (1 chute na mão)
1. Botão direito no POST → **Send to Repeater**.
2. Troque `"senha":"111111"` → Send → observe `401`; troque para `123456` → `200`.
3. É o `bruteforce_simples.py` feito à mão — ótimo para explicar `status_code`.

## 4. Intruder (wordlist sem código)
1. Send to Intruder → Positions: marque só o valor da senha → Attack type **Sniper**.
2. Payloads → Load → `material_bruteforce/senhas.txt` → Start attack.
3. Coluna Status: ache o `200` no meio dos `401`. Compare com saída do Python.

| Recurso | Para que |
| :--- | :--- |
| Proxy history | Prova que Python mandou N POSTs. |
| Repeater | Testa 1 credencial editada. |
| Intruder Sniper + `senhas.txt` | Repete o ataque do script, sem programar. |

## 5. Saída esperada
Intruder com 5 payloads: 4× `401` (Length ~50) + 1× `200` (Length maior). Mesmo resultado do script, mas sem `break`, contador ou relatório — aí entra a comparação com Python.

---

## 6. Anexo A — Docker por Aluno + HTTP em Claro + Sem Interferência

**Docker local:** cada aluno roda `cd banco_web && docker compose up --build` na própria máquina; o Burp escuta `127.0.0.1:8080` só localmente, então o proxy de um não afeta o outro. Se dois alunos usarem a mesma porta Burp, cada um usa a sua — não há Burp central.

**HTTP mostra tudo no Burp:** sem TLS, o Proxy exibe JSON, `token` base64 e `Set-Cookie: nb_session` sem precisar instalar CA (a CA só será necessária no guia C2 HTTPS). Use o Decoder do Burp para `base64 -d` no token.

**Isolamento:** o POST vai de `127.0.0.1 → 127.0.0.1:8002` dentro do host; nada trafega até o colega. Em rede chaveada ninguém intercepta o Burp alheio.
