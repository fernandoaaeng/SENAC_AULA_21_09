# Exercicio 4 — Simule um log de eventos
# Rode de dentro desta pasta, 3 vezes: python exercicio.py
# O arquivo log.txt cresce sem apagar as linhas anteriores.

from datetime import datetime


def registrar(mensagem):
    agora = datetime.now().strftime("%H:%M:%S")
    with open("log.txt", "a", encoding="utf-8") as arq:
        arq.write(f"{agora} - {mensagem}\n")


registrar("Script iniciado")
registrar("login ok")
registrar("login falhou")

print("Linhas adicionadas em log.txt:")
with open("log.txt", encoding="utf-8") as arq:
    print(arq.read())
