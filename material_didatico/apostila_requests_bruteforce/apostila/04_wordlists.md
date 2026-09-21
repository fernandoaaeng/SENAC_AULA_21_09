# 4. O que é uma wordlist

Uma **wordlist** (lista de palavras) é um arquivo de texto com **uma senha candidata por linha**. Não é magia: é estatística e preguiça humana. Pessoas repetem `123456`, `senha`, o nome do time, o ano de nascimento. Quem ataca senhas **não começa** gerando `a`, `b`, `aa`… começa pelo que já deu certo em vazamentos anteriores.

## De onde vêm essas listas

Vazamentos de empresas e fóruns, ao longo dos anos, despejaram milhões de senhas reais. Pesquisadores e equipes de segurança **compilam** esses dados (já públicos) em arquivos de estudo. Nomes que você vai ouvir:

- **rockyou.txt** — lista famosa, enorme, associada a um vazamento antigo; usada em laboratórios e certificações.
- **SecLists** — coleção de listas (senhas, usuários, caminhos web) mantida pela comunidade de segurança para testes.

Você **não precisa baixar** nada disto agora. O professor pode entregar um arquivo pequeno (`senhas_fracas.txt` com 20 linhas) para a prática. Listas gigantes travam máquina ruim e desviam o foco da aula.

## Por que “funciona tão bem” contra senha fraca

Três motivos, todos humanos:

1. **Poucas senhas cobrem muita gente.** Em vazamentos, as dezenas de senhas mais comuns aparecem dezenas de milhares de vezes.
2. **A política do sistema ajuda o atacante.** Se não há limite de tentativas, dá para testar milhares de chutes. O laboratório foi feito exatamente assim — de propósito.
3. **A senha não está “escondida no código”.** Está no banco, mas se estiver em **texto puro** (outro erro proposital do laboratório), um vazamento do arquivo já entrega tudo. Mesmo *com* hash, senha fraca ainda cai para wordlist + tentativa de login ou para quebra offline.

## Dicionário versus força bruta pura

Os dois nomes se misturam no dia a dia. Vale separar:

| Tipo | O que testa | Velocidade típica | Quando “ganha” |
|---|---|---|---|
| **Ataque de dicionário** | Só o que está na wordlist (e variações leves: `Senha1`, `senha123`) | Rápido | Senha previsível |
| **Força bruta pura** | Todas as combinações: `a`…`z`, números, símbolos, tamanho 1, 2, 3… | Explode combinatoriamente | Senha curta e aleatória ainda pode cair; senha longa e aleatória, na prática, não |

Exemplo de explosão: só minúsculas, 6 caracteres → 26⁶ ≈ 308 milhões de palpite. Oito caracteres já vai para bilhões. Por isso a defesa séria pede senha **longa** (ou gerenciador + senha aleatória), **não** “troque a letra por @”.

Nesta apostila, quando falamos “brute force de login” na aula, na verdade o exercício mental é quase sempre **dicionário contra o endpoint `/login`**: poucas senhas, muitas vezes as do seed.

## Wordlist não é só senha

Existem listas de **usuários** (`admin`, `ana`, `root`), de **caminhos** (`/admin`, `/login`) e de **payloads**. O princípio é o mesmo: testar o que é comum antes do que é raro.

## Resumo do capítulo

Wordlist = arquivo de candidatos. Dicionário ≠ brute force pura. Senha fraca + API sem limite de tentativas = cenário que o laboratório simula para você **enxergar o log do defensor**.

## Exercícios

1. Escreva dez senhas que você considera fracas (não use senhas reais suas). Justifique cada uma em uma frase.
2. Com calculadora: se o alfabeto tem 10 dígitos (`0-9`) e a senha tem 4 dígitos, quantas combinações a força bruta pura testaria no pior caso?
3. Por que uma wordlist de 20 linhas pode descobrir `admin123` mais depressa do que gerar todas as senhas de 8 caracteres?
4. O professor some com o seed da tabela. O que muda na sua estratégia de estudo: wordlist genérica ou força bruta pura de 12 caracteres? Por quê?
