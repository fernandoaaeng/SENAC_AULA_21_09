# 3. Manipulação de arquivos em Python

Rede e arquivo são os dois “mundos externos” do programa: um é o servidor HTTP; o outro é o disco. Em segurança, arquivos aparecem o tempo todo: **lista de senhas para estudo**, **exportação de log**, **relatório**.

## Abrir do jeito certo: `with`

`open()` pede ao sistema operacional um arquivo. Se você esquecer de fechar, o arquivo pode ficar travado. O `with` fecha sozinho, mesmo se der erro no meio.

```python
# "r" = read (leitura). encoding="utf-8" evita problema de acento no Windows
with open("mensagem.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()  # lê o arquivo inteiro numa string
print(conteudo)
```

## Ler linha a linha

Wordlists e logs são, no fundo, **um item por linha**. Não jogue um arquivo de 14 milhões de linhas na memória de uma vez se puder evitar. O `for` no arquivo lê aos poucos:

```python
with open("senhas.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        senha = linha.strip()  # tira \n e espaços nas pontas
        if not senha:
            continue  # pula linha vazia
        print("Li a senha (estudo):", senha)
```

`strip()` é obrigatório. Sem ele, `"123456\n"` **não é** igual a `"123456"`.

## Escrever (`w`) versus anexar (`a`)

| Modo | O que faz | Quando usar |
|---|---|---|
| `"w"` | Cria ou **apaga** o conteúdo antigo e escreve do zero | Relatório novo do dia |
| `"a"` | **Anexa** no final (append) | Log que não pode perder histórico |
| `"r"` | Só lê | Wordlist |

```python
# Recria o arquivo toda vez — perigoso se for log
with open("relatorio.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("Primeira linha\n")

# Acrescenta sem apagar o que já existia
with open("acessos.log", "a", encoding="utf-8") as arquivo:
    arquivo.write("2026-09-21 10:00:00 | ana | falha | 192.168.0.10\n")
```

Esquecer o `\n` cola tudo numa linha só. Logs viram um novelo.

## CSV simples (sem biblioteca extra)

CSV é texto com colunas separadas por vírgula. Dá para escrever na mão:

```python
with open("tentativas.csv", "a", encoding="utf-8") as arquivo:
    usuario = "ana"
    resultado = "falha"
    arquivo.write(f"{usuario},{resultado}\n")
```

Depois você abre no Excel ou no LibreOffice. Cuidado: se o próprio dado tiver vírgula, a coluna quebra — para a aula, evite vírgula nos campos.

## Por que isso entra nesta disciplina

1. **Ler wordlist** = `for linha in arquivo` + `strip()`.
2. **Gravar log** = modo `"a"` + uma linha por evento (data, usuário, IP, sucesso).
3. O laboratório `banco_web_aula_21_09` já grava `data/acessos.log` no **servidor**. O cliente (seu script) também pode gravar o que *ele* tentou, do lado de quem dispara as requisições — são dois pontos de vista do mesmo fenômeno.

## Resumo do capítulo

`with open(...)` é o padrão. Leia linha a linha. `strip()` nas senhas. `"a"` para log, `"w"` só quando quiser recomeçar o arquivo.

## Exercícios

1. Crie `nomes.txt` com cinco nomes, um por linha. Escreva um programa que imprima cada nome em maiúsculas.
2. Explique o que acontece se você abrir um log com `"w"` no segundo dia de aula.
3. Escreva um programa que anexe em `aula.log` a frase `iniciou o programa` e o horário (use o módulo `datetime`). Rode duas vezes e abra o arquivo.
4. Uma wordlist tem uma linha em branco no meio. Sem `if not senha: continue`, o que seu laço faria com essa linha?
