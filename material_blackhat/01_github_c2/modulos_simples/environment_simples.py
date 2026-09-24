"""Módulo simples: coleta variáveis de ambiente (versão segura para sala)."""
import os


def run(**args):
    print("[*] In environment_simples module.")
    # Retorna apenas chaves (não valores) para não expor segredos no log da aula.
    chaves = sorted(os.environ.keys())
    return str(chaves)
