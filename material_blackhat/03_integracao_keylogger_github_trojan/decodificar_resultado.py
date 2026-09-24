#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decodifica arquivo .data do trojan (base64 -> texto).
Uso: python decodificar_resultado.py data/abc/<arquivo>.data
"""
import base64
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Uso: python {Path(__file__).name} <arquivo.data>")
    sys.exit(1)

caminho = Path(sys.argv[1])
raw = caminho.read_bytes()
try:
    decoded = base64.b64decode(raw).decode('utf-8', errors='replace')
except Exception as e:
    print(f"[!] Falha ao decodificar: {e}")
    sys.exit(1)

print(decoded)
