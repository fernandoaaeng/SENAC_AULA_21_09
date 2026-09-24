#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulador LOCAL de C2 modular (versão iniciante).
Não usa GitHub, token ou rede: lê config_simulado.json
e importa módulos da pasta modulos_simples/.
Uso exclusivo em laboratório.
"""
import importlib
import json
import threading
import time
from datetime import datetime
from pathlib import Path

# 1. Parâmetros de configuração
ARQUIVO_CONFIG = "config_simulado.json"
PASTA_MODULOS = "modulos_simples"
PASTA_RESULTADOS = "data_simulada"

print("=" * 60)
print("   SIMULADOR LOCAL DE C2 (sem GitHub)")
print("=" * 60)

# 2. Leitura da lista de tarefas
with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
    tarefas = json.load(f)

print(f"[+] Tarefas recebidas: {[t['module'] for t in tarefas]}")


# 3. Função que executa um módulo isolado
def executar_modulo(nome):
    print(f"[*] Executando módulo: {nome}")
    try:
        modulo = importlib.import_module(f"{PASTA_MODULOS}.{nome}")
    except ModuleNotFoundError:
        print(f"[-] Módulo '{nome}' não encontrado. Pulando.")
        return
    resultado = modulo.run()
    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destino = Path(PASTA_RESULTADOS) / f"{nome}_{carimbo}.txt"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(str(resultado), encoding="utf-8")
    print(f"[+] Resultado de '{nome}' salvo em: {destino}")


# 4. Disparo em paralelo + espera
threads = []
for tarefa in tarefas:
    th = threading.Thread(target=executar_modulo, args=(tarefa["module"],))
    th.start()
    threads.append(th)
    time.sleep(1)

for th in threads:
    th.join()

print("Ciclo concluído. Verifique a pasta data_simulada/")
