# Exercicio 5 — Leia um CSV e imprima colunas
# Rode de dentro desta pasta: python exercicio.py

import csv

print("Nome e curso de cada aluno:")
with open("alunos.csv", encoding="utf-8") as arq:
    leitor = csv.DictReader(arq)
    for linha in leitor:
        print(linha["nome"], "-", linha["curso"])

print()
print('Desafio — so alunos do curso "Seguranca":')
with open("alunos.csv", encoding="utf-8") as arq:
    leitor = csv.DictReader(arq)
    for linha in leitor:
        if linha["curso"] == "Seguranca":
            print(linha["nome"], "-", linha["curso"])
