# Passo a passo da aula — Requests e arquivos

Este README e o roteiro do aluno. O slide tem a mesma sequencia; use os dois juntos.

Slide (na pasta da aula):

`material_didatico/Requests, Arquivos e Brute Force — Aula 21 09.html`

Abra com um clique duplo no navegador.

---

## 1. O que acontece na aula

1. Voce abre o slide.
2. O professor sobe o **NexusBank Corporate** e escreve o IP no quadro.
3. Voce testa o acesso no navegador (passo 3 abaixo).
4. Faz os exercicios **1 a 8** no seu computador (nao precisam da rede).
5. Nos exercicios **9 e 10**, troca o IP no script e conversa com a API da sala.

O professor **nao pede** para voce subir o banco. Ele sobe; voce so usa o IP.

---

## 2. Preparar o Python (uma vez)

No terminal, na pasta `exercicios_requests_arquivos`:

```
pip install -r requirements.txt
```

Isso instala a biblioteca `requests`, usada a partir do exercicio 9.

Confira se o Python responde:

```
python --version
```

---

## 3. Anotar o IP do professor

Quando o professor passar o IP, teste no navegador **antes** dos exercicios 9 e 10:

| O que abrir | Endereco |
| --- | --- |
| Site do banco | `http://IP:8080` |
| Saude da API | `http://IP:8002/api/saude` |
| Documentacao (Swagger) | `http://IP:8002/docs` |

Resposta esperada em `/api/saude`:

```json
{"status": "ok", "sistema": "NexusBank Corporate"}
```

Se nao abrir, avise o professor. Nao invente outro IP e nao teste em outro computador.

Nos scripts 9 e 10, troque a linha:

```python
URL = "http://127.0.0.1:8002"
```

pelo IP da aula, por exemplo:

```python
URL = "http://192.168.0.10:8002"
```

Use o numero que o professor passar, nao este exemplo.

---

## 4. Contas de teste da aula (seed)

So para o exercicio 10, com o servidor da sala:

| Usuario | Senha | Papel |
| --- | --- | --- |
| ana | 123456 | cliente |
| bruno | senha123 | cliente |

---

## 5. Como rodar cada exercicio

Entre na pasta do exercicio **antes** de rodar. Os arquivos (`alunos.txt`, CSV, etc.) ficam nessa pasta.

```
cd 01_ler_txt
python exercicio.py
```

Depois volte e entre na proxima:

```
cd ..
cd 02_contar_nomes
python exercicio.py
```

---

## 6. Roteiro dos exercicios

### Bloco 01 — Arquivos

#### Exercicio 1 — Leia um `.txt` e imprima cada nome

Pasta: `01_ler_txt`  
Arquivo pronto: `alunos.txt` (Ana, Bruno, Carlos)

1. Abra `alunos.txt` e confira se tem um nome por linha.
2. Rode `python exercicio.py`.
3. O script imprime cada nome.
4. Desafio (ja no script): imprime tambem o numero da linha (`1 - Ana`).

O `strip()` tira o `\n` do final da linha.

#### Exercicio 2 — Conte informacoes do arquivo

Pasta: `02_contar_nomes`

1. Rode `python exercicio.py`.
2. Veja o total de nomes e quantos comecam com **A**.
3. Desafio: o script pede uma letra no terminal. Digite, por exemplo, `B`.

#### Exercicio 3 — Escreva uma lista em um arquivo

Pasta: `03_escrever_lista`

1. Rode `python exercicio.py`.
2. Abra `nomes.txt` e confira: um nome por linha.
3. Desafio: abra tambem `nomes_numerados.txt` (`1. Ana`, `2. Bruno`...).

Modo `"w"` cria o arquivo (ou apaga o que ja existia) e escreve do zero.

#### Exercicio 4 — Simule um log de eventos

Pasta: `04_log_eventos`

1. Rode `python exercicio.py`.
2. Rode **mais duas vezes** (tres no total).
3. Abra `log.txt`: as linhas novas entram no final. O arquivo nao e apagado.
4. Desafio (ja no script): cada execucao registra horario + mensagens diferentes.

Modo `"a"` e append: adiciona no final, sem apagar o que ja tinha.

#### Exercicio 5 — Leia um CSV e imprima colunas

Pasta: `05_ler_csv`  
Arquivo pronto: `alunos.csv`

CSV = texto organizado em colunas, separado por virgula. A primeira linha e o cabecalho.

1. Rode `python exercicio.py`.
2. O script imprime nome e curso de cada aluno.
3. Desafio: imprime so os alunos do curso `Seguranca`.

#### Exercicio 6 — Escreva o seu proprio CSV

Pasta: `06_escrever_csv`

1. Rode `python exercicio.py`.
2. Abra `saida.csv` e confira o cabecalho (`nome,idade`) e as linhas.

---

### Bloco 02 — Diretorios

#### Exercicio 7 — Liste so os arquivos `.txt`

Pasta: `07_listar_txt`

Nesta pasta ja existem extras: `.txt`, `.csv` e `.py`.

1. Rode `python exercicio.py`.
2. Devem aparecer so os arquivos que terminam em `.txt`.
3. Desafio: o script conta quantos arquivos tem de cada extensao.

#### Exercicio 8 — Encontre o arquivo "esquecido"

Pasta: `08_encontrar_arquivo`

O arquivo `senhas.txt` esta escondido em uma subpasta. O `os.listdir(".")` so ve a pasta atual; o `os.walk(".")` entra nas subpastas.

1. Rode `python exercicio.py`.
2. O script deve dizer o caminho completo, por exemplo:

   `.\pasta_c\escondido\senhas.txt`

---

### Bloco 03 — Requests (precisa do IP do professor)

Instale o `requests` se ainda nao instalou (`pip install -r requirements.txt`).
Troque o `URL` nos dois scripts pelo IP da aula.

#### Exercicio 9 — Bata no primeiro endpoint

Pasta: `09_get_saude`

1. Troque `127.0.0.1` pelo IP do professor, se o servidor nao estiver na sua maquina.
2. Rode `python exercicio.py`.
3. Confira: status `200` e o JSON `{"status": "ok", "sistema": "NexusBank Corporate"}`.
4. Desafio: o script tambem chama `/nada`. Anote o status (em geral `404`).

| Campo | O que e |
| --- | --- |
| `status_code` | Numero da resposta (`200` ok, `404` nao existe, `401` nao autorizado) |
| `.json()` | Resposta convertida em dicionario Python |
| `.text` | Resposta crua, como texto |

#### Exercicio 10 — Logue com as contas de teste

Pasta: `10_login`

1. Troque o IP no script, como no exercicio 9.
2. Rode `python exercicio.py`.
3. Login da Ana: `POST /login` com `ana` / `123456`. Status esperado: `200`.
4. Desafio: o script tambem loga o Bruno (`bruno` / `senha123`).

Resposta esperada (campos parecidos com estes):

```json
{"ok": true, "usuario": "ana", "papel": "cliente", "token": "..."}
```

O `json=dados` do `requests` monta o JSON e o cabecalho certo sozinho.

---

## 7. Mapa rapido das pastas

| Pasta | Exercicio | Precisa da API? |
| --- | --- | --- |
| `01_ler_txt` | 1 — ler `.txt` | Nao |
| `02_contar_nomes` | 2 — contar nomes | Nao |
| `03_escrever_lista` | 3 — escrever `.txt` | Nao |
| `04_log_eventos` | 4 — log com horario | Nao |
| `05_ler_csv` | 5 — ler CSV | Nao |
| `06_escrever_csv` | 6 — escrever CSV | Nao |
| `07_listar_txt` | 7 — listar `.txt` | Nao |
| `08_encontrar_arquivo` | 8 — `os.walk()` | Nao |
| `09_get_saude` | 9 — `GET /api/saude` | Sim |
| `10_login` | 10 — `POST /login` | Sim |

---

## 8. Se algo nao funcionar

- **`python` nao e reconhecido:** tente `py exercicio.py` (Windows).
- **`No such file` / arquivo nao encontrado:** voce precisa estar **dentro** da pasta do exercicio.
- **Exercicio 9 ou 10 nao conecta:** confira o IP, a porta `8002` e se o professor ja subiu o servidor.
- **Site abre e a API nao:** use `http://IP:8002/api/saude` no navegador. Se falhar, avise o professor.

---

## 9. Regra da aula

Estes scripts so podem apontar para o servidor do laboratorio, com o IP que o professor passar.
Nao use outro endereco, site real ou rede de terceiros.

O restante da aula (a partir do slide do bloco 04) acompanha o professor ao vivo. Este README cobre os exercicios 1 a 10.
