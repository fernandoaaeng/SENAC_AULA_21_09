# Exercicio 1 — Leia um .txt e imprima cada nome
# Rode de dentro desta pasta: python exercicio.py

print("Nomes no arquivo:")
with open("alunos.txt", encoding="utf-8") as arq:
    for linha in arq:
        print(linha.strip())

print()
print("Desafio — nome e numero da linha:")
with open("alunos.txt", encoding="utf-8") as arq:
    numero = 1
    for linha in arq:
        nome = linha.strip()
        if nome:
            print(numero, "-", nome)
            numero = numero + 1
