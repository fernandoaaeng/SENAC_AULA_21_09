# Exercicio 9 — Bata no primeiro endpoint
# Troque o IP se o servidor estiver no computador do professor.
# Rode de dentro desta pasta: python exercicio.py
# Precisa: pip install requests

import requests

# Troque pelo IP passado em aula, se o servidor nao estiver na sua maquina
URL = "http://127.0.0.1:8002"

resposta = requests.get(f"{URL}/api/saude")
print("GET /api/saude")
print("status_code:", resposta.status_code)
print("json:", resposta.json())

print()
print("Desafio — caminho que nao existe:")
resposta_errada = requests.get(f"{URL}/nada")
print("GET /nada")
print("status_code:", resposta_errada.status_code)
print("texto:", resposta_errada.text)
