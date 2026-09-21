# Exercicio 6 — Escreva o seu proprio CSV
# Rode de dentro desta pasta: python exercicio.py

import csv

alunos = [
    {"nome": "Ana", "idade": 22},
    {"nome": "Bruno", "idade": 25},
    {"nome": "Carlos", "idade": 19},
    {"nome": "Diana", "idade": 21},
]

with open("saida.csv", "w", newline="", encoding="utf-8") as arq:
    escritor = csv.DictWriter(arq, fieldnames=["nome", "idade"])
    escritor.writeheader()
    escritor.writerows(alunos)

print("Arquivo saida.csv criado.")
print()
print("Conteudo:")
with open("saida.csv", encoding="utf-8") as arq:
    print(arq.read())
