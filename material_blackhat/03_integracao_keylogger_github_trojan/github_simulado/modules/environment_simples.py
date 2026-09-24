"""Módulo simulado para integração local (só chaves, sem segredos)."""
import os


def run(**args):
    print("[*] In environment_simples module.")
    return str(sorted(os.environ.keys()))
