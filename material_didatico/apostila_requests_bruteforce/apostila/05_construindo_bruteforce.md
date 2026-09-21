# 5. Como um ataque a senhas fracas é montado (conceitos)

Este capítulo mostra **como as peças se encaixam na cabeça de quem ataca um login**. Ele **não** entrega um script completo pronto para disparar milhares de senhas contra um servidor. Motivo: um laço `for` + `requests.post` + wordlist **é** um programa de ataque. Isso só pode existir, se existir, **na sua máquina, no laboratório, sob comando do professor** — não como material copiável desta apostila.

O que você **vai** sair sabendo: (1) uma tentativa de login legítima em Python; (2) ler senhas de um arquivo; (3) registrar resultado em log; (4) o **fluxo** que junta as três coisas.

## Passo A — Uma única tentativa (cliente de API)

Qualquer aplicativo honesto faz isto: um `POST` com JSON.

```python
import requests

# Ajuste o IP se o professor subir o laboratório em outro computador da rede
URL = "http://127.0.0.1:8002/login"

def tentar_login(usuario, senha):
    """Envia UM palpite. Devolve o status HTTP (200, 401, ...)."""
    try:
        resposta = requests.post(
            URL,
            json={"usuario": usuario, "senha": senha},
            timeout=5,
        )
        return resposta.status_code
    except requests.exceptions.RequestException as erro:
        print("Rede:", erro)
        return None

# Teste manual — uma senha só, como se você tivesse esquecido e tentasse de novo
codigo = tentar_login("ana", "teste")
print("Status:", codigo)
```

Interpretação no laboratório:

- `200` → combinação aceita.
- `401` → combinação recusada.
- `None` → você nem falou com o servidor (ele está fora do ar?).

## Passo B — Ler candidatos do disco (sem enviar)

Isto é só o capítulo 3 de novo, isolado. Treine **sem** rede:

```python
def carregar_wordlist(caminho):
    senhas = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            texto = linha.strip()
            if texto:
                senhas.append(texto)
    return senhas

lista = carregar_wordlist("senhas_fracas.txt")
print("Quantidade de senhas no arquivo:", len(lista))
print("Primeira:", lista[0] if lista else "(arquivo vazio)")
```

Arquivo de exemplo `senhas_fracas.txt` (invente o seu; **não** coloque senhas reais):

```text
123456
senha
admin
qwerty
```

## Passo C — Registrar o que aconteceu

Do lado do **atacante** (ou do aluno testando), um CSV local ajuda a estudar. Do lado do **servidor**, o laboratório já grava `data/acessos.log`. São logs diferentes.

```python
from datetime import datetime

def registrar(caminho, usuario, senha_usada, status):
    agora = datetime.now().isoformat(timespec="seconds")
    with open(caminho, "a", encoding="utf-8") as arquivo:
        # Não grave senha em log de produção de verdade; aqui é laboratório didático
        arquivo.write(f"{agora},{usuario},{status}\n")
```

## O fluxo que a aula discute (pseudocódigo)

Juntar A+B+C em um único laço é o ataque de dicionário contra o endpoint. Em pseudocódigo — **não execute como receita contra nada além do laboratório autorizado**:

```text
usuario_alvo ← (definido pelo professor)
para cada senha em wordlist:
    status ← POST /login com usuario_alvo e senha
    anotar no log (hora, usuario, status, IP de origem se souber)
    se status = 200:
        parar  (encontrou)
        avisar o professor / registrar no relatório da aula
    senão:
        continuar
```

Detalhes que o “script de produção” costuma ter e que **não** precisamos copiar aqui: pausa entre tentativas, vários usuários, cores no terminal, threads paralelas (pior para o servidor e para o aluno). Na aula, o valor está em **entender o laço**, não em turbinar o golpe.

## O que o laboratório faz de propósito para este fluxo funcionar

Releia os comentários `# VULNERAVEL DE PROPOSITO` no código do `banco_web_aula_21_09`:

- senha em texto puro;
- sem teto de tentativas;
- sem bloqueio de conta;
- contas fracas no seed (se o professor não as removeu).

Se **qualquer** uma dessas defesas existisse de verdade (hash + rate limit + MFA), o mesmo fluxo ficaria inútil ou muito barulhento nos logs.

## Resumo do capítulo

Login em Python = um `POST`. Wordlist = arquivo. Ataque de dicionário = laço que combina os dois. Esta apostila ensina as peças e o fluxo; o professor decide se monta o laço completo **ao vivo**, só contra o alvo da sala.

## Exercícios

1. Rode o Passo A contra o laboratório ligado. Anote status para senha errada.
2. Crie `senhas_fracas.txt` com 8 linhas e use o Passo B para contar quantas linhas não vazias existem.
3. Desenhe no caderno o fluxograma do pseudocódigo (losango: “status é 200?”).
4. Cite duas mudanças no **servidor** que fariam esse fluxo falhar ou ficar evidente em minutos (antecipando o capítulo 8).
