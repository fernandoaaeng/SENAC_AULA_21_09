# Exercicio 10 — Logue na aplicacao com as contas de teste da aula
# Troque o IP se o servidor estiver no computador do professor.
# Rode de dentro desta pasta: python exercicio.py
# Precisa: pip install requests

import requests

# Troque pelo IP passado em aula, se o servidor nao estiver na sua maquina
URL = "http://127.0.0.1:8002"

print("Login da Ana (conta de teste da aula):")
resposta_ana = requests.post(
    f"{URL}/login",
    json={"usuario": "ana", "senha": "123456"},
)
print("status_code:", resposta_ana.status_code)
print("json:", resposta_ana.json())

print()
print("Desafio — login do Bruno (conta de teste da aula):")
resposta_bruno = requests.post(
    f"{URL}/login",
    json={"usuario": "bruno", "senha": "senha123"},
)
print("status_code:", resposta_bruno.status_code)
print("json:", resposta_bruno.json())
