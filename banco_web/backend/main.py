# NexusBank Internet Banking — laboratorio (propositalmente vulneravel).
# Porta 8002. uvicorn main:app --host 0.0.0.0 --port 8002

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from db import iniciar_banco
from schemas import ClienteCreate, ContaCreate, LoginIn, UsuarioCreate, ValorOperacao
from services.auth_service import AuthService
from services.banco_service import BancoService

app = FastAPI(
    title="NexusBank Corporate",
    version="2.0.0",
    description="Alvo didatico de laboratorio. Nao usar como modelo de sistema seguro.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth = AuthService()
banco = BancoService()

COOKIE = "nb_session"
PAPEIS_STAFF = ("operador", "admin")


@app.on_event("startup")
def ao_iniciar():
    iniciar_banco()


def ip_cliente(request: Request):
    encaminhado = request.headers.get("x-forwarded-for")
    if encaminhado:
        return encaminhado.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "desconhecido"


def extrair_token(request: Request, token_query: str | None = None):
    # VULNERAVEL DE PROPOSITO: aceita token no header, cookie e query string.
    header = request.headers.get("authorization") or ""
    if header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    cookie = request.cookies.get(COOKIE)
    if cookie:
        return cookie
    return token_query


def gravar_cookie(response: Response, token: str):
    # VULNERAVEL DE PROPOSITO: cookie sem HttpOnly e sem Secure.
    response.set_cookie(
        COOKIE,
        token,
        httponly=False,
        secure=False,
        samesite="lax",
        path="/",
    )


def exigir_sessao(request: Request, papeis=None, token_query: str | None = None):
    token = extrair_token(request, token_query)
    sessao = auth.sessao_por_token(token)
    if sessao is None:
        raise HTTPException(status_code=401, detail="Sessao invalida.")
    if papeis and sessao["papel"] not in papeis:
        raise HTTPException(status_code=403, detail="Perfil sem permissao.")
    return sessao


def resposta_login(registro, ip, response: Response):
    token = auth.criar_sessao(registro, ip)
    gravar_cookie(response, token)
    return {
        "ok": True,
        "usuario": registro["usuario"],
        "papel": registro["papel"],
        "cliente_cpf": registro["cliente_cpf"],
        "token": token,
    }


@app.get("/api/saude")
def saude():
    return {"status": "ok", "sistema": "NexusBank Corporate"}


@app.post("/login")
@app.post("/api/auth/login")
def login(dados: LoginIn, request: Request, response: Response):
    # VULNERAVEL DE PROPOSITO: sem rate limiting — a mesma conta pode ser tentada infinitas vezes.
    usuario = auth.autenticar(dados.usuario, dados.senha, ip_cliente(request))
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario ou senha invalidos.")
    if usuario["papel"] != "cliente":
        raise HTTPException(
            status_code=403,
            detail="Use o acesso corporativo para este perfil.",
        )
    return resposta_login(usuario, ip_cliente(request), response)


@app.post("/admin/login")
@app.post("/api/auth/backoffice/login")
def admin_login(dados: LoginIn, request: Request, response: Response):
    usuario = auth.autenticar(
        dados.usuario,
        dados.senha,
        ip_cliente(request),
        papeis_ok=PAPEIS_STAFF,
    )
    if usuario is None:
        raise HTTPException(status_code=401, detail="Acesso corporativo invalido.")
    return resposta_login(usuario, ip_cliente(request), response)


@app.post("/api/auth/logout")
def logout(request: Request, response: Response, token: str | None = Query(None)):
    atual = extrair_token(request, token)
    auth.encerrar_sessao(atual)
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@app.get("/api/auth/me")
def eu(request: Request, token: str | None = Query(None)):
    sessao = exigir_sessao(request, token_query=token)
    return {
        "usuario": sessao["usuario"],
        "papel": sessao["papel"],
        "cliente_cpf": sessao["cliente_cpf"],
        "token": sessao["token"],
        "ip": sessao["ip"],
        "criado_em": sessao["criado_em"],
    }


def _exigir_admin_legado(usuario, senha, request: Request):
    # VULNERAVEL DE PROPOSITO: logs sem token; so usuario/senha no corpo (ou query).
    registro = auth.autenticar(
        usuario,
        senha,
        ip_cliente(request),
        papeis_ok=("admin",),
    )
    if registro is None:
        raise HTTPException(status_code=401, detail="Admin invalido.")
    return registro


@app.post("/admin/logs")
def admin_logs_post(dados: LoginIn, request: Request):
    _exigir_admin_legado(dados.usuario, dados.senha, request)
    return auth.listar_logs()


@app.get("/admin/logs")
def admin_logs_get(
    request: Request,
    usuario: str = Query(...),
    senha: str = Query(...),
):
    _exigir_admin_legado(usuario, senha, request)
    return auth.listar_logs()


@app.get("/api/admin/logs")
def admin_logs_sessao(request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=("admin",), token_query=token)
    return auth.listar_logs()


@app.get("/api/admin/sessoes")
def admin_sessoes(request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=("admin",), token_query=token)
    return auth.listar_sessoes()


@app.get("/api/admin/usuarios")
def admin_usuarios(request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=("admin",), token_query=token)
    return auth.listar_usuarios()


@app.post("/api/admin/usuarios", status_code=201)
def admin_criar_usuario(
    dados: UsuarioCreate,
    request: Request,
    token: str | None = Query(None),
):
    exigir_sessao(request, papeis=("admin",), token_query=token)
    criado = auth.criar_usuario(dados.usuario, dados.senha, dados.papel, dados.cliente_cpf)
    if criado is None:
        raise HTTPException(status_code=400, detail="Usuario ja existe.")
    return criado


@app.get("/api/me/contas")
def minhas_contas(request: Request, token: str | None = Query(None)):
    sessao = exigir_sessao(request, papeis=("cliente",), token_query=token)
    if not sessao["cliente_cpf"]:
        return []
    return banco.listar_contas(cpf=sessao["cliente_cpf"])


def _conta_do_cliente(sessao, numero):
    conta = banco.pegar_conta(numero)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada.")
    if sessao["papel"] == "cliente" and conta["cpf"] != sessao["cliente_cpf"]:
        raise HTTPException(status_code=403, detail="Conta de outro titular.")
    return conta


@app.get("/api/me/contas/{numero}")
def minha_conta(numero: int, request: Request, token: str | None = Query(None)):
    sessao = exigir_sessao(request, papeis=("cliente",), token_query=token)
    return _conta_do_cliente(sessao, numero)


@app.post("/api/me/contas/{numero}/depositar")
def meu_deposito(
    numero: int,
    dados: ValorOperacao,
    request: Request,
    token: str | None = Query(None),
):
    sessao = exigir_sessao(request, papeis=("cliente",), token_query=token)
    _conta_do_cliente(sessao, numero)
    ok, resultado = banco.depositar(numero, dados.valor)
    if not ok:
        raise HTTPException(status_code=400, detail=resultado)
    return resultado


@app.post("/api/me/contas/{numero}/sacar")
def meu_saque(
    numero: int,
    dados: ValorOperacao,
    request: Request,
    token: str | None = Query(None),
):
    sessao = exigir_sessao(request, papeis=("cliente",), token_query=token)
    _conta_do_cliente(sessao, numero)
    ok, resultado = banco.sacar(numero, dados.valor)
    if not ok:
        raise HTTPException(status_code=400, detail=resultado)
    return resultado


@app.post("/api/me/contas/{numero}/render")
def meu_rendimento(numero: int, request: Request, token: str | None = Query(None)):
    sessao = exigir_sessao(request, papeis=("cliente",), token_query=token)
    _conta_do_cliente(sessao, numero)
    ok, erro, resultado = banco.render(numero)
    if not ok:
        raise HTTPException(status_code=400, detail=erro)
    return resultado


@app.get("/api/clientes")
def listar_clientes(request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    return banco.listar_clientes()


@app.post("/clientes", status_code=201)
@app.post("/api/clientes", status_code=201)
def cadastrar_cliente(
    dados: ClienteCreate,
    request: Request,
    token: str | None = Query(None),
):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    cliente = banco.cadastrar_cliente(dados.nome, dados.cpf)
    if cliente is None:
        raise HTTPException(status_code=400, detail="CPF ja cadastrado.")
    return cliente


@app.post("/contas", status_code=201)
@app.post("/api/contas", status_code=201)
def criar_conta(
    dados: ContaCreate,
    request: Request,
    token: str | None = Query(None),
):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    conta = banco.criar_conta(dados.cpf, dados.tipo, dados.saldo_inicial)
    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente nao encontrado. Cadastre o cliente primeiro.",
        )
    return conta


@app.get("/contas")
@app.get("/api/contas")
def listar_contas(request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    return banco.listar_contas()


@app.get("/contas/{numero}")
@app.get("/api/contas/{numero}")
def detalhe_conta(numero: int, request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    conta = banco.pegar_conta(numero)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta nao encontrada.")
    return conta


@app.post("/contas/{numero}/depositar")
@app.post("/api/contas/{numero}/depositar")
def depositar(
    numero: int,
    dados: ValorOperacao,
    request: Request,
    token: str | None = Query(None),
):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    ok, resultado = banco.depositar(numero, dados.valor)
    if not ok:
        status = 404 if resultado == "Conta nao encontrada." else 400
        raise HTTPException(status_code=status, detail=resultado)
    return resultado


@app.post("/contas/{numero}/sacar")
@app.post("/api/contas/{numero}/sacar")
def sacar(
    numero: int,
    dados: ValorOperacao,
    request: Request,
    token: str | None = Query(None),
):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    ok, resultado = banco.sacar(numero, dados.valor)
    if not ok:
        status = 404 if resultado == "Conta nao encontrada." else 400
        raise HTTPException(status_code=status, detail=resultado)
    return resultado


@app.post("/contas/{numero}/render")
@app.post("/api/contas/{numero}/render")
def render_poupanca(numero: int, request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=PAPEIS_STAFF, token_query=token)
    ok, erro, resultado = banco.render(numero)
    if not ok:
        status = 404 if erro == "Conta nao encontrada." else 400
        raise HTTPException(status_code=status, detail=erro)
    return resultado


@app.delete("/contas/{numero}")
@app.delete("/api/contas/{numero}")
def excluir_conta(numero: int, request: Request, token: str | None = Query(None)):
    exigir_sessao(request, papeis=("admin",), token_query=token)
    if not banco.excluir_conta(numero):
        raise HTTPException(status_code=404, detail="Conta nao encontrada.")
    return {"detail": f"Conta {numero} excluida."}
