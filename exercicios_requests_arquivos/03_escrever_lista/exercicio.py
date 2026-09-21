# Exercicio 3 — Escreva uma lista em um arquivo
# Rode de dentro desta pasta: python exercicio.py

nomes = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]

with open("nomes.txt", "w", encoding="utf-8") as arq:
    for nome in nomes:
        arq.write(nome + "\n")

print("Arquivo nomes.txt criado.")

print()
print("Desafio — linhas numeradas:")
with open("nomes_numerados.txt", "w", encoding="utf-8") as arq:
    numero = 1
    for nome in nomes:
        arq.write(f"{numero}. {nome}\n")
        numero = numero + 1

print("Arquivo nomes_numerados.txt criado.")
print()
print("Conteudo de nomes_numerados.txt:")
with open("nomes_numerados.txt", encoding="utf-8") as arq:
    print(arq.read())
