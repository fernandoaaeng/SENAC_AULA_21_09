# 1. Introdução: o que é uma requisição HTTP

Antes de escrever qualquer linha com a biblioteca `requests`, vale travar uma ideia simples: **programa A pede algo; programa B responde**. Isso é o modelo **cliente-servidor**. O navegador que você usa para abrir o banco web é um cliente. O FastAPI que sobe na porta 8002 é o servidor.

## Cliente e servidor, como um restaurante

Imagine que você senta em um restaurante:

1. Você (cliente) escolhe um prato no cardápio.
2. O garçom leva o pedido à cozinha (servidor).
3. A cozinha devolve o prato — ou avisa que o item acabou.

Na web, o “cardápio” são as **rotas** da API (`/login`, `/contas`, `/admin/logs`). O “pedido” é uma **requisição HTTP**. O “prato ou o aviso” é a **resposta HTTP**, com um **código de status** (deu certo, senha errada, página não existe, etc.).

## Os quatro pedaços que você precisa reconhecer

### Método

O método diz **o tipo de ação**:

| Método | Analogia no restaurante | Uso típico |
|---|---|---|
| `GET` | “Me mostre o cardápio / o estado da mesa” | Consultar dados |
| `POST` | “Quero este prato / enviar este formulário” | Enviar dados (login, cadastro) |
| `PUT` / `PATCH` | “Troque o ponto da carne” | Atualizar |
| `DELETE` | “Cancele o pedido” | Remover |

No laboratório do banco, o login é um `POST /login`: você **envia** usuário e senha, não só “olha” a página.

### Rota (também chamada de endpoint)

É o caminho depois do endereço do servidor. Se o servidor está em `http://127.0.0.1:8002`, então:

- `http://127.0.0.1:8002/login` → rota `/login`
- `http://127.0.0.1:8002/docs` → rota `/docs` (Swagger)

A rota sozinha não basta: o servidor precisa aceitar aquele **método** naquela rota. `GET /login` pode nem existir; o laboratório espera `POST /login`.

### Status code

Número de três dígitos na resposta. Você não precisa decorar a tabela inteira agora. Memorize estes:

| Código | Significado aproximado |
|---|---|
| `200` | OK — a operação deu certo |
| `201` | Criado — um recurso novo nasceu (ex.: cliente cadastrado) |
| `400` | Pedido malformado (dado inválido) |
| `401` | Não autenticado — usuário ou senha errados, ou falta login |
| `404` | Não encontrado |
| `500` | Erro interno do servidor |

No brute force “de filme”, o atacante olha exatamente isso: **401 = tente outra senha**, **200 = achei**.

### Corpo em JSON

Muitas APIs modernas não usam formulário HTML clássico. Elam esperam um **JSON** no corpo:

```json
{"usuario": "ana", "senha": "123456"}
```

JSON é texto estruturado: chaves entre aspas, dois-pontos, valores. Em Python isso vira um `dict`.

A resposta também pode vir em JSON:

```json
{"ok": true, "usuario": "ana", "eh_admin": false}
```

ou, em falha:

```json
{"detail": "Usuario ou senha invalidos."}
```

## Cabeçalhos (visão rápida)

Além do corpo, a requisição carrega **cabeçalhos**. Um que você vai usar logo:

`Content-Type: application/json` — “o que estou enviando é JSON”.

Sem esse aviso, alguns servidores não interpretam o corpo direito.

## Resumo do capítulo

Uma requisição HTTP junta **método + rota + (opcionalmente) corpo**. A resposta junta **status code + (opcionalmente) JSON**. A biblioteca `requests` só empacota isso em Python. O próximo capítulo ensina a empacotar.

## Exercícios

1. Escreva com suas palavras a diferença entre **cliente** e **servidor**. Dê um exemplo que não seja o navegador (por exemplo: aplicativo de banco no celular).
2. O laboratório expõe `POST /login`. Explique por que um `GET /login` provavelmente **não** faria sentido para enviar senha.
3. Relacione: um login com senha errada no FastAPI do laboratório tende a devolver qual status? E um login certo?
4. Monte, no papel, o JSON de um `POST /admin/login` com usuário `admin` e uma senha qualquer (não precisa acertar a senha real).
