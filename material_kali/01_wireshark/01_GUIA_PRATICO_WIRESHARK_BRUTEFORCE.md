# Guia Prático: Wireshark no Brute Force (NexusBank `/login`)

**Laboratório:** NexusBank (`http://127.0.0.1:8002/login` ou `http://192.168.x.x:8002/login`)
**Ferramenta:** Wireshark / `tshark`
**Script observado:** `material_bruteforce/bruteforce_simples.py`

---

> ⚠️ Tráfego de laboratório contém **senhas de teste em texto claro** (HTTP sem TLS). Use só `senhas.txt` de aula.

---

## 1. O Modelo no Fio (o que o Python realmente manda)

```text
[Script Python]                          [Servidor NexusBank]
      |  POST /login {"usuario":"ana","senha":"111111"}  |
      | -----------------------------------------------> |
      |  HTTP/1.1 401 Unauthorized                      |
      | <----------------------------------------------- |
      |  POST /login {"usuario":"ana","senha":"123456"}  |
      | -----------------------------------------------> |
      |  HTTP/1.1 200 OK                                |
      | <----------------------------------------------- |
```

Cada `requests.post()` vira: handshake TCP (se keep-alive reaproveita) + 1 requisição HTTP + 1 resposta com `status_code`.

## 2. Captura Passo a Passo (localhost funciona?)

1. **Escolha da interface:**
   * Kali tudo-local: capture em `lo` (loopback).
   * Windows + `127.0.0.1`: instale Npcap com loopback ou **prefira o IP da LAN**: suba o backend em `0.0.0.0` e use `http://192.168.0.10:8002/login` no script. Aí capture em `eth0/Wi-Fi`.
2. **Filtro de captura (antes de começar):** `tcp port 8002`
3. **Inicie a captura**, rode em outro terminal:
   ```bash
   python bruteforce_simples.py
   ```
4. **Pare** e aplique filtro de exibição:
   ```
   tcp.port == 8002 && http
   ```

| Filtro | Para que serve |
| :--- | :--- |
| `tcp.port == 8002` | Isola só o NexusBank. |
| `http.request.method == POST` | Mostra só os chutes (sem respostas). |
| `http.response.code == 401` | Conta erros. |
| `http.response.code == 200` | Acha o acerto. |
| `json.member contains "ana"` | Se o dissector JSON estiver ativo. |

## 3. Lendo um Chute (Follow TCP Stream)

1. Clique num `POST /login` → botão direito → **Follow → TCP Stream**.
2. Você verá:
   ```http
   POST /login HTTP/1.1
   Host: 127.0.0.1:8002
   Content-Type: application/json
   Content-Length: 33

   {"usuario": "ana", "senha": "123456"}
   ---
   HTTP/1.1 200 OK
   ```
3. Repita para um `401` e compare o corpo.

## 4. Contando Tentativas sem Python (Statistics)

* **Statistics → Conversations → TCP:** 1 conversa com N pacotes = N chutes (keep-alive).
* **Statistics → HTTP → Requests:** conta `POST /login`.
* Via `tshark` (ver `tshark_comandos.sh`):
  ```bash
  tshark -r captura.pcap -Y "http.response.code==401" | wc -l
  tshark -r captura.pcap -Y "http.response.code==200" -T fields -e http.file_data
  ```

## 5. Saída Esperada

Para `senhas.txt` com 4 linhas até `123456`:
* 4 `POST /login`, 3 respostas `401`, 1 resposta `200`.
* Tempo entre POSTs ≈ tempo do `requests.post` + `print` (veja coluna `Time since previous segment`).

> 📌 **Ponte Blue Team:** mesmo sem ler o `.py`, o defensor vê rajada de `401` do mesmo IP em frações de segundo → regra de rate-limit + alerta. É o exercício 3.4 do bruteforce, agora com prova no fio.

---

## 6. Anexo A — Docker Local, HTTP em Texto Claro e Isolamento em Sala

**A. Docker por aluno (sem servidor central).** Cada máquina sobe o próprio lab:
```bash
cd banco_web
docker compose up --build
curl http://127.0.0.1:8002/api/saude
```
A API publica `8002:8002` e escuta em `0.0.0.0`, então o script e o Wireshark usam o alvo local. Não há disputa de porta entre alunos porque cada Docker é um host distinto.

**B. Por ser só HTTP, o Wireshark vê tudo.** Sem TLS, o Follow TCP Stream mostra:
```http
POST /login → {"usuario": "ana", "senha": "123456"}
HTTP/1.1 200 OK → {"ok": true, "papel": "cliente", "token": "YW5hOmNsaWVudGU6..."}
Set-Cookie: nb_session=YW5hOm...; Path=/
```
Ou seja: senha, token `base64(usuario:papel:data)` e cookie sem `HttpOnly/Secure` — tudo decodificável em aula. No C2 GitHub (HTTPS) o mesmo Wireshark só veria SNI + tamanho/hora.

**C. Sala cheia na mesma rede: pego o tráfego do colega? Não.**
Rede chaveada não espelha unicast para todos; `127.0.0.1` nem sai da máquina e `192.168.x.x → 192.168.x.x:8002` (próprio IP) é resolvido internamente. Cada um filtra pelo próprio IP para provar:
```
tcp.port == 8002 && ip.addr == <seu-IP>
ip.src == <seu-IP> && http.request.method == POST
```
Se aparecer outro IP, é broadcast/mDNS — ignore. Não façam ARP spoofing entre colegas.
