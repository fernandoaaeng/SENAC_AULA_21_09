#!/usr/bin/env python3
"""Compara tempo Hydra (manual) vs Python (auto) — preencha após rodar cada um."""
import time

if __name__ == "__main__":
    print("Rode: time python bruteforce_simples.py  -> anote T_PY")
    print("Rode: time hydra ...                     -> anote T_HYDRA")
    # Exemplo de preenchimento:
    T_PY = float(input("Tempo Python (s): ") or 0)
    T_HYDRA = float(input("Tempo Hydra (s): ") or 0)
    if T_HYDRA > 0:
        print(f"Hydra foi {T_PY/T_HYDRA:.1f}x mais rápido (ou <1 = Python venceu).")
    print("Discuta: velocidade vs controle/relatório (ver guia §4).")
