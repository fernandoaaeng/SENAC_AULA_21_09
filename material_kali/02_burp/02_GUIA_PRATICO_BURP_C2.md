# Guia Prático: Burp no C2 GitHub (MITM consentido em lab)

**Laboratório:** `git_trojan.py` → `https://api.github.com`
**Requisito:** instalar CA do Burp no Python (`certifi`) + `HTTPS_PROXY=127.0.0.1:8080`

> Só em lab com token descartável. Sem a CA, o `github3.py` aborta com `SSLError` — esse erro já é a aula.

## 1. Por que precisa da CA?
Wireshark mostrou TLS opaco. O Burp faz MITM: apresenta cert próprio para o Python e outro para o GitHub. O Python só confia se a CA PortSwigger estiver no bundle `certifi`.

## 2. Setup
1. Burp → Proxy → Options → exporte `cacert.der` → converta para `.pem`.
2. Kali:
   ```bash
   export HTTPS_PROXY=http://127.0.0.1:8080 HTTP_PROXY=http://127.0.0.1:8080
   python -c "import certifi; print(certifi.where())"
   cat ~/cacert.pem >> $(python -c "import certifi; print(certifi.where())")
   ```
3. Rode `git_trojan.py` (sleep curto para aula). Veja em history: `GET /repos/.../contents/config/abc.json` (base64), `GET .../modules/keylogger.py`, `PUT/POST .../contents/data/abc/*.data`.

## 3. O que observar
* Request: JSON com `content` em base64 → use **Decoder** do Burp para decodificar (é o `abc.json` e o `.py`).
* Response `201 Created` no `create_file` = beacon com sucesso.
* Compare com Wireshark: mesmo beacon, agora legível porque você tem a chave (CA).

| Sem CA | Com CA |
| :--- | :--- |
| `SSLError` + nada no history | JSON/base64 visível, decodificável |

## 4. Limites
Se o lab ativar cert-pinning ou token com IP allowlist, o MITM falha — ótimo gancho para aula defensiva.
