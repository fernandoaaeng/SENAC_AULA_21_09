"""Módulo simples: lista arquivos do diretório atual."""
import os


def run(**args):
    print("[*] In dirlister_simples module.")
    files = os.listdir(".")
    return str(files)
