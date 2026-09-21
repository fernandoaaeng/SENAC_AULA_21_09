# NexusBank Corporate — laboratorio (propositalmente vulneravel)

> **Esta aplicacao e propositalmente vulneravel.** Ela existe para aula pratica
> de laboratorio. Nao use este codigo como referencia de como proteger um sistema real.

Este diretorio e o material da aula (API + Angular + PostgreSQL). Pode ser publicado
como repositorio separado para os alunos.

A API sobe na porta **8002** e a interface na **8080**, para conviver com o `banco_web`
na 8000 se os dois estiverem na mesma maquina.

## Estrutura do repositorio

```
.
├── docker-compose.yml      # sobe Postgres + API + Angular
├── README.md
├── backend/                # FastAPI
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   ├── models/
│   ├── services/
│   ├── data/               # logs de acesso (volume)
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/               # Angular (Internet Banking + backoffice)
    ├── src/
    ├── nginx.conf
    └── Dockerfile
```

## O que o sistema cobre

- Front em **Angular**, com navegacao segmentada:
  - site institucional
  - Internet Banking (cliente)
  - Backoffice (operador / admin)
- Persistencia em **PostgreSQL** (clientes, contas, usuarios, sessoes e logs).
- Papeis: `cliente`, `operador`, `admin`.
- Token de sessao devolvido no JSON, gravado no `localStorage` e em cookie fraco.
- CRUDs de cliente/conta na area autenticada do backoffice.

## Vulnerabilidades propositais (didaticas)

- Senhas em **texto puro**, sem hash.
- Sem limite de tentativas (rate limiting) e sem bloqueio de conta.
- Credenciais fracas no seed.
- Token previsivel (Base64 de `usuario:papel:timestamp`), sem assinatura e sem expiracao.
- Token aceito no header `Authorization`, no cookie `nb_session` e na query `?token=`.
- Cookie sem `HttpOnly` e sem `Secure`.
- Rota legada de logs (`/admin/logs`) sem token: usuario/senha no corpo (POST) ou na query (GET).

Cada escolha esta comentada no codigo com `# VULNERAVEL DE PROPOSITO: ...`.

## Como subir

Com Docker (recomendado):

```bash
docker compose up --build
```

- Interface: http://localhost:8080
- API / Swagger: http://localhost:8002/docs
- PostgreSQL: localhost:5432 (usuario `nexus`, senha `nexus`, banco `nexusbank`)

Sem Docker (API + Postgres local + Angular):

```bash
cd backend
python -m pip install -r requirements.txt
set DATABASE_URL=postgresql://nexus:nexus@localhost:5432/nexusbank
python -m uvicorn main:app --host 0.0.0.0 --port 8002
```

Em outro terminal:

```bash
cd frontend
npm install
npm start
```

- Angular (proxy para a API): http://localhost:4200

## Credenciais de seed

| Usuario | Senha | Papel | Contas |
|---|---|---|---|
| ana | 123456 | cliente | poupanca 1001 |
| bruno | senha123 | cliente | corrente 1002 |
| carlos | qwerty | cliente | nenhuma |
| operador | op123 | operador | — |
| admin | admin123 | admin | — |

O professor decide se remove essas contas do seed em `backend/db.py`.

## Rotas da API

| Metodo | Rota | Quem | O que faz |
|---|---|---|---|
| `POST` | `/login` ou `/api/auth/login` | cliente | Login do Internet Banking |
| `POST` | `/admin/login` ou `/api/auth/backoffice/login` | operador/admin | Login corporativo |
| `POST` | `/api/auth/logout` | autenticado | Encerra a sessao |
| `GET` | `/api/auth/me` | autenticado | Dados da sessao |
| `GET` | `/api/me/contas` | cliente | Contas do titular |
| `POST` | `/api/me/contas/{n}/depositar` | cliente | Deposito |
| `POST` | `/api/me/contas/{n}/sacar` | cliente | Saque |
| `GET/POST` | `/api/clientes` | operador/admin | CRUD de clientes |
| `GET/POST` | `/api/contas` | operador/admin | Contas e abertura |
| `DELETE` | `/api/contas/{n}` | admin | Exclui conta |
| `GET` | `/api/admin/logs` | admin + token | Logs |
| `GET/POST` | `/admin/logs` | admin + senha | Logs (legado, sem token) |
| `GET` | `/api/admin/sessoes` | admin | Tokens ativos |
| `GET/POST` | `/api/admin/usuarios` | admin | Usuarios e papeis |

As rotas antigas `/clientes` e `/contas` continuam, agora exigindo sessao de staff.

## Uso etico e legal

Esta aplicacao so deve ser usada **dentro da rede do laboratorio**, contra a instancia
subida pelo professor, com autorizacao explicita da aula. Atacar qualquer sistema sem
autorizacao e crime (Marco Civil da Internet; art. 154-A do Codigo Penal).

Este repositorio **nao inclui** roteiro de ferramenta de ataque nem script de forca bruta.
O laboratorio discute o alvo (esta API) e as defesas que faltam; procedimentos ofensivos
ficam a cargo do professor, ao vivo, se a instituicao autorizar.
