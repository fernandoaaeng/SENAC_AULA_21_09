# Exercicio 8 — Encontre o arquivo "esquecido"
# Rode de dentro desta pasta: python exercicio.py

import os

alvo = "senhas.txt"

print(f'Procurando "{alvo}" nas pastas...')
encontrado = False

for pasta, subpastas, arquivos in os.walk("."):
    if alvo in arquivos:
        caminho = os.path.join(pasta, alvo)
        print("Encontrado em:", caminho)
        encontrado = True

if not encontrado:
    print("Arquivo nao encontrado.")
