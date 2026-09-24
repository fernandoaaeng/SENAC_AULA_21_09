#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integração SIMULADA keylogger + C2 (versão iniciante).
Pastas locais fingem ser o GitHub: push/pull sem token ou rede.
Uso exclusivo em laboratório.
"""
import importlib
import json
import shutil
from datetime import datetime
from pathlib import Path

# 1. Pastas que fingem ser o GitHub
BASE = Path("github_simulado")
(BASE / "config").mkdir(parents=True, exist_ok=True)
(BASE / "modules").mkdir(parents=True, exist_ok=True)
(BASE / "data" / "abc").mkdir(parents=True, exist_ok=True)

# Garante __init__.py para import funcionar
(BASE / "__init__.py").touch(exist_ok=True)
(BASE / "modules" / "__init__.py").touch(exist_ok=True)

# 2. PUSH: publica config com 3 módulos
config = [
    {"module": "dirlister_simples"},
    {"module": "environment_simples"},
    {"module": "keylogger_simples"},
]
(BASE / "config" / "abc.json").write_text(
    json.dumps(config, indent=2), encoding="utf-8"
)
print("[push] abc.json publicado com 3 módulos.")

# 3. PULL: vítima baixa o config
tarefas = json.loads((BASE / "config" / "abc.json").read_text(encoding="utf-8"))
print(f"[pull] Tarefas recebidas: {[t['module'] for t in tarefas]}")

# 4. EXEC: importa e roda cada módulo
for t in tarefas:
    nome = t["module"]
    print(f"[*] Attempting to retrieve {nome}")
    try:
        mod = importlib.import_module(f"github_simulado.modules.{nome}")
    except ModuleNotFoundError:
        print(f"[-] Módulo '{nome}' não encontrado. Pulando.")
        continue
    resultado = mod.run()
    carimbo = datetime.now().isoformat().replace(":", "-")
    destino = BASE / "data" / "abc" / f"{carimbo}_{nome}.txt"
    destino.write_text(str(resultado)[:2000], encoding="utf-8")
    print(f"[+] Resultado de '{nome}' salvo em: {destino}")

print("Integração simulada concluída. Abra github_simulado/data/abc/")
