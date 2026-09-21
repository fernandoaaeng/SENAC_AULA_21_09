# Exercicio 2 — Conte informacoes do arquivo
# Rode de dentro desta pasta: python exercicio.py

total = 0
comeca_com_a = 0

with open("alunos.txt", encoding="utf-8") as arq:
    for linha in arq:
        nome = linha.strip()
        if nome:
            total = total + 1
            if nome.upper().startswith("A"):
                comeca_com_a = comeca_com_a + 1

print("Total:", total)
print('Nomes que comecam com "A":', comeca_com_a)

letra = input("Desafio — digite uma letra: ").strip()
if letra:
    letra = letra[0]
    quantidade = 0
    with open("alunos.txt", encoding="utf-8") as arq:
        for linha in arq:
            nome = linha.strip()
            if nome and nome.upper().startswith(letra.upper()):
                quantidade = quantidade + 1
    print(f'Nomes que comecam com "{letra.upper()}":', quantidade)
