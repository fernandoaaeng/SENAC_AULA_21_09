# Guia Prático: Wireshark no C2 GitHub (o que dá para ver com HTTPS)

**Laboratório:** `material_blackhat/01_github_c2/git_trojan.py` → `api.github.com:443`
**Ferramenta:** Wireshark (capture em `eth0`, não em `lo`)

---

> ⚠️ GitHub é **HTTPS**: conteúdo (token, `abc.json`, `.py`, `.data`) é criptografado. O valor da aula é mostrar **metadados**.

## 1. O que aparece vs o que NÃO aparece

```text
[Vítima] --TLS ClientHello SNI=api.github.com--> [GitHub]  (VISÍVEL: SNI, IP, hora, tamanho)
         <--ServerHello + certificado--                     (VISÍVEL)
         --Application Data (GET config/abc.json + base64)-- (OPACO: só tamanho/hora)
         --Application Data (POST create_file .data)--       (OPACO)
```

| Visível | Criptografado |
| :--- | :--- |
| DNS para `api.github.com`, SNI no ClientHello, IPs `140.82.112.0/20`, horários, tamanhos, intervalos 30m–3h | Token, JSON, código dos módulos, resultados |

## 2. Passo a passo
1. Capture em `eth0` com filtro `host api.github.com`.
2. Rode `github_c2_simples.py` (local, sem rede — controle negativo: **nada** aparece) e depois `git_trojan.py` em lab (aparecem rajadas TLS).
3. Filtros:
   ```
   tls.handshake.extensions_server_name contains "github"
   tls && ip.addr == 140.82.112.0/20
   ```
4. Em Statistics → Conversations, anote duração e bytes por beacon. O sleep aleatório vira intervalos irregulares — exatamente o que EDR procura.

## 3. Saída esperada
* 1 burst TLS por ciclo (GET config + GET modules + POST data).
* Nada legível em Follow TCP Stream (só bytes TLS).
* Prova pedagógica: "C2 bem feito não se detecta pelo conteúdo, e sim por **comportamento** (destino raro + periodicidade + tamanho)".

> 📌 Para ver o conteúdo, use o Burp (módulo 02) com CA instalada — ele faz MITM consentido em lab.
