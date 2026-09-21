# 2. A biblioteca `requests` em Python

O Python, sozinho, já consegue abrir URLs (módulo `urllib`). Na prática de curso técnico, a biblioteca **`requests`** é mais legível: menos código, mesma ideia (mandar HTTP e ler a resposta).

## Instalação

No terminal, com o ambiente virtual ativo se você estiver usando um:

```bash
python -m pip install requests
```

No laboratório, se o projeto já tiver `requirements.txt` com FastAPI, o `requests` **não vem junto** — ele é biblioteca de *cliente*. Instale à parte no seu script de testes.

## Um GET simples

`GET` pede um recurso. Exemplo: listar contas do banco (rota pública no laboratório).

```python
import requests  # importa a biblioteca de cliente HTTP

# timeout evita o programa “travar para sempre” se o servidor não responder
resposta = requests.get(
    "http://127.0.0.1:8002/contas",
    timeout=5,
)

print(resposta.status_code)  # ex.: 200
print(resposta.text)         # texto cru (string)
print(resposta.json())       # se o corpo for JSON, vira list/dict em Python
```

- `status_code` é o número (int).
- `text` é sempre string. Bom para HTML ou mensagem solta.
- `json()` **interpreta** o texto como JSON. Se o corpo não for JSON, essa linha dispara erro — por isso existe `try/except`.

## Um POST com JSON (login)

O login do laboratório espera JSON. Em `requests`, isso é o parâmetro `json=`:

```python
import requests

url = "http://127.0.0.1:8002/login"
corpo = {"usuario": "ana", "senha": "123456"}  # dict Python vira JSON

resposta = requests.post(url, json=corpo, timeout=5)

print(resposta.status_code)
if resposta.status_code == 200:
    dados = resposta.json()
    print("Logou:", dados.get("usuario"))
else:
    print("Falhou:", resposta.text)
```

`json=corpo` já coloca o cabeçalho `Content-Type: application/json` para você.

## Erros de rede versus erros de senha

São coisas diferentes:

- **Senha errada**: o servidor *respondeu*. Você recebe `401`. Isso **não** é exceção de rede.
- **Servidor desligado, cabo de rede, DNS**: o cliente *nem consegue falar*. Aí sim entra `requests.exceptions.RequestException`.

```python
import requests

url = "http://127.0.0.1:8002/login"
try:
    resposta = requests.post(
        url,
        json={"usuario": "ana", "senha": "errada"},
        timeout=5,
    )
except requests.exceptions.RequestException as erro:
    # Cai aqui se não houver conexão, timeout, etc.
    print("Falha de rede:", erro)
else:
    # Só chega aqui se houve resposta HTTP
    print("Status HTTP:", resposta.status_code)
```

`timeout=5` significa: espere no máximo 5 segundos. Sem timeout, um servidor “zumbi” segura sua aula inteira.

## Outros detalhes úteis

- `resposta.headers` — dicionário de cabeçalhos da resposta.
- `resposta.raise_for_status()` — se o status for 4xx/5xx, gera exceção. Útil quando você *não* quer tratar 401 na mão; no estudo de login, em geral **você quer** olhar o 401.

## Resumo do capítulo

`requests.get` consulta; `requests.post` envia. Sempre leia `status_code`. Use `json()` só quando a resposta for JSON. Separe **falha de rede** (exceção) de **falha de autenticação** (401).

## Exercícios

1. Instale `requests` e faça um `GET` em `https://httpbin.org/get` (serviço público de teste). Imprima o `status_code`.
2. Com o laboratório **ligado**, faça `GET http://127.0.0.1:8002/contas` e conte quantas contas vieram no JSON.
3. Faça dois `POST /login`: um com senha certamente errada e um com uma conta do seed (se o professor liberar o seed). Anote os dois status codes.
4. Desligue o servidor e rode o mesmo `POST`. O que aparece: `401` ou uma `RequestException`? Explique.
