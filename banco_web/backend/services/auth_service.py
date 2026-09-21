# Autenticacao propositalmente fraca para laboratorio (aula autorizada).

import base64
from datetime import datetime, timezone

from db import LOG_PATH, conectar


class AuthService:
    def buscar_usuario(self, usuario):
        with conectar() as conn:
            row = conn.execute(
                """
                SELECT usuario, senha, papel, cliente_cpf
                FROM usuarios
                WHERE usuario = %s
                """,
                (usuario,),
            ).fetchone()
        return dict(row) if row else None

    def autenticar(self, usuario, senha, ip, papeis_ok=None):
        # VULNERAVEL DE PROPOSITO: sem limite de tentativas e sem bloqueio de conta.
        registro = self.buscar_usuario(usuario)
        ok = False
        if registro is not None:
            # VULNERAVEL DE PROPOSITO: comparacao da senha em texto puro.
            ok = registro["senha"] == senha
            if ok and papeis_ok and registro["papel"] not in papeis_ok:
                ok = False
        self.registrar_tentativa(usuario, ok, ip)
        if not ok:
            return None
        return registro

    def criar_sessao(self, registro, ip):
        # VULNERAVEL DE PROPOSITO: token previsivel, sem assinatura e sem expiracao.
        agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        bruto = f"{registro['usuario']}:{registro['papel']}:{agora}"
        token = base64.b64encode(bruto.encode("utf-8")).decode("ascii")
        with conectar() as conn:
            conn.execute(
                """
                INSERT INTO sessoes (token, usuario, papel, ip, criado_em)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (token) DO UPDATE
                SET usuario = EXCLUDED.usuario, papel = EXCLUDED.papel, ip = EXCLUDED.ip
                """,
                (token, registro["usuario"], registro["papel"], ip, agora),
            )
        return token

    def sessao_por_token(self, token):
        if not token:
            return None
        with conectar() as conn:
            row = conn.execute(
                "SELECT token, usuario, papel, ip, criado_em FROM sessoes WHERE token = %s",
                (token,),
            ).fetchone()
        if not row:
            return None
        usuario = self.buscar_usuario(row["usuario"])
        if usuario is None:
            return None
        return {
            "token": row["token"],
            "usuario": usuario["usuario"],
            "papel": usuario["papel"],
            "cliente_cpf": usuario["cliente_cpf"],
            "ip": row["ip"],
            "criado_em": row["criado_em"],
        }

    def encerrar_sessao(self, token):
        if not token:
            return
        with conectar() as conn:
            conn.execute("DELETE FROM sessoes WHERE token = %s", (token,))

    def listar_sessoes(self):
        with conectar() as conn:
            rows = conn.execute(
                """
                SELECT token, usuario, papel, ip, criado_em
                FROM sessoes
                ORDER BY criado_em DESC
                """
            ).fetchall()
        return [dict(r) for r in rows]

    def listar_usuarios(self):
        with conectar() as conn:
            rows = conn.execute(
                """
                SELECT usuario, papel, cliente_cpf
                FROM usuarios
                ORDER BY usuario
                """
            ).fetchall()
        return [dict(r) for r in rows]

    def criar_usuario(self, usuario, senha, papel, cliente_cpf=None):
        with conectar() as conn:
            existe = conn.execute(
                "SELECT 1 FROM usuarios WHERE usuario = %s",
                (usuario,),
            ).fetchone()
            if existe:
                return None
            conn.execute(
                """
                INSERT INTO usuarios (usuario, senha, papel, cliente_cpf)
                VALUES (%s, %s, %s, %s)
                """,
                (usuario, senha, papel, cliente_cpf),
            )
        return {"usuario": usuario, "papel": papel, "cliente_cpf": cliente_cpf}

    def registrar_tentativa(self, usuario, sucesso, ip):
        agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        with conectar() as conn:
            conn.execute(
                """
                INSERT INTO logs_acesso (usuario, sucesso, ip, criado_em)
                VALUES (%s, %s, %s, %s)
                """,
                (usuario, 1 if sucesso else 0, ip, agora),
            )

        linha = f"{agora} | usuario={usuario} | sucesso={sucesso} | ip={ip}\n"
        with LOG_PATH.open("a", encoding="utf-8") as arquivo:
            arquivo.write(linha)

    def listar_logs(self, limite=50):
        with conectar() as conn:
            rows = conn.execute(
                """
                SELECT usuario, sucesso, ip, criado_em
                FROM logs_acesso
                ORDER BY id DESC
                LIMIT %s
                """,
                (limite,),
            ).fetchall()
        return [dict(r) for r in rows]
