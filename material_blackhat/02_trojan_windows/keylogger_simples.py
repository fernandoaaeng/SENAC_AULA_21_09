#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keylogger SIMULADO para sala de aula (multiplataforma, sem hook/admin).
Troca pyWinhook por input() + StringIO + timestamp.
Uso exclusivo em laboratório.
"""
from datetime import datetime
from io import StringIO
import platform

# 1. Parâmetros de configuração
RODADAS = 5
ARQUIVO_LOG = "log_simples.txt"

print("=" * 60)
print("   KEYLOGGER SIMULADO (sem hook, via input)")
print("=" * 60)

# 2. Prepara buffer em memória
buf = StringIO()
buf.write(f"[INFO] Maquina: {platform.node()} | Sistema: {platform.system()}\n")

# 3. Loop de captura simulada
for i in range(1, RODADAS + 1):
    texto = input(f"[{i}/{RODADAS}] Digite algo (ou 'sair'): ")
    if texto.strip().lower() == "sair":
        break
    if not texto.strip():
        print("[!] Linha vazia ignorada.")
        continue
    agora = datetime.now().strftime("%H:%M:%S")
    if texto.startswith("[PASTE]"):
        buf.write(f"[{agora}] [PASTE] - {texto[7:]}\n")
    else:
        buf.write(f"[{agora}] {texto}\n")

# 4. Salva e devolve o log
log = buf.getvalue()
with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
    f.write(log)

print("=" * 60)
print(log)
print(f"[+] Log salvo em '{ARQUIVO_LOG}'.")
