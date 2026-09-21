from typing import Literal, Optional

from pydantic import BaseModel


class ClienteCreate(BaseModel):
    nome: str
    cpf: str


class ContaCreate(BaseModel):
    cpf: str
    tipo: Literal["p", "c"]
    saldo_inicial: float


class ValorOperacao(BaseModel):
    valor: float


class LoginIn(BaseModel):
    usuario: str
    senha: str


class UsuarioCreate(BaseModel):
    usuario: str
    senha: str
    papel: Literal["cliente", "operador", "admin"] = "cliente"
    cliente_cpf: Optional[str] = None
