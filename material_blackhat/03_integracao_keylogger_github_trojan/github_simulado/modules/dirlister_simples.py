"""Módulo simulado para integração local."""
import os


def run(**args):
    print("[*] In dirlister_simples module.")
    return str(os.listdir("."))
