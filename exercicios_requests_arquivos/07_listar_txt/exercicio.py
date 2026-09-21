# Exercicio 7 — Liste so os arquivos .txt de uma pasta
# Rode de dentro desta pasta: python exercicio.py

import os

print("Arquivos .txt desta pasta:")
for nome_arquivo in os.listdir("."):
    if nome_arquivo.endswith(".txt"):
        print(nome_arquivo)

print()
print("Desafio — quantidade de arquivos por extensao:")
contagem = {}
for nome_arquivo in os.listdir("."):
    if os.path.isfile(nome_arquivo):
        if "." in nome_arquivo:
            extensao = nome_arquivo.rsplit(".", 1)[1]
        else:
            extensao = "(sem extensao)"
        if extensao not in contagem:
            contagem[extensao] = 0
        contagem[extensao] = contagem[extensao] + 1

for extensao, quantidade in contagem.items():
    print(f".{extensao}: {quantidade}" if extensao != "(sem extensao)" else f"{extensao}: {quantidade}")
