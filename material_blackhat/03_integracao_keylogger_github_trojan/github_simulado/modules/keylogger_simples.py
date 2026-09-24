"""Keylogger simulado NÃO-interativo para integração local (sem input)."""
from datetime import datetime


def run(**args):
    print("[*] In keylogger_simples module (simulado, sem hook).")
    agora = datetime.now().strftime("%H:%M:%S")
    return f"[{agora}] [notepad@LAB-PC01] ola mundo simulado\n[{agora}] [PASTE] - senha123_teste"
