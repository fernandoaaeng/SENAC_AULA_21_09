from decimal import Decimal

from db import conectar


def _conta_row(row):
    if row is None:
        return None
    tipo = row["tipo"]
    saldo = float(row["saldo"])
    return {
        "numero": int(row["numero"]),
        "titular": row["titular"],
        "cpf": row["cliente_cpf"],
        "tipo": tipo,
        "saldo": saldo,
        "limite": float(row["limite"]) if tipo == "corrente" else 0.0,
    }


class BancoService:
    def cadastrar_cliente(self, nome, cpf):
        with conectar() as conn:
            existe = conn.execute(
                "SELECT 1 FROM clientes WHERE cpf = %s",
                (cpf,),
            ).fetchone()
            if existe:
                return None
            conn.execute(
                "INSERT INTO clientes (cpf, nome) VALUES (%s, %s)",
                (cpf, nome),
            )
        return {"nome": nome, "cpf": cpf}

    def listar_clientes(self):
        with conectar() as conn:
            rows = conn.execute(
                "SELECT cpf, nome FROM clientes ORDER BY nome"
            ).fetchall()
        return [dict(r) for r in rows]

    def criar_conta(self, cpf, tipo, saldo):
        tipo_db = "poupanca" if tipo == "p" else "corrente"
        with conectar() as conn:
            cliente = conn.execute(
                "SELECT cpf, nome FROM clientes WHERE cpf = %s",
                (cpf,),
            ).fetchone()
            if cliente is None:
                return None
            numero = conn.execute(
                "SELECT nextval('contas_numero_seq') AS numero"
            ).fetchone()["numero"]
            limite = 200 if tipo_db == "corrente" else 0
            taxa = 0.01 if tipo_db == "poupanca" else 0
            conn.execute(
                """
                INSERT INTO contas (numero, cliente_cpf, tipo, saldo, limite, taxa_rendimento)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (numero, cpf, tipo_db, Decimal(str(saldo)), limite, taxa),
            )
        return self.pegar_conta(numero)

    def listar_contas(self, cpf=None):
        sql = """
            SELECT c.numero, c.cliente_cpf, c.tipo, c.saldo, c.limite, cl.nome AS titular
            FROM contas c
            JOIN clientes cl ON cl.cpf = c.cliente_cpf
        """
        params = []
        if cpf:
            sql += " WHERE c.cliente_cpf = %s"
            params.append(cpf)
        sql += " ORDER BY c.numero"
        with conectar() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [_conta_row(r) for r in rows]

    def pegar_conta(self, numero):
        try:
            numero = int(numero)
        except (TypeError, ValueError):
            return None
        with conectar() as conn:
            row = conn.execute(
                """
                SELECT c.numero, c.cliente_cpf, c.tipo, c.saldo, c.limite, cl.nome AS titular
                FROM contas c
                JOIN clientes cl ON cl.cpf = c.cliente_cpf
                WHERE c.numero = %s
                """,
                (numero,),
            ).fetchone()
        return _conta_row(row)

    def depositar(self, numero, valor):
        if valor <= 0:
            return False, "Valor de deposito invalido."
        conta = self.pegar_conta(numero)
        if conta is None:
            return False, "Conta nao encontrada."
        with conectar() as conn:
            conn.execute(
                "UPDATE contas SET saldo = saldo + %s WHERE numero = %s",
                (Decimal(str(valor)), conta["numero"]),
            )
        return True, self.pegar_conta(numero)

    def sacar(self, numero, valor):
        if valor <= 0:
            return False, "Saldo insuficiente ou valor invalido!"
        conta = self.pegar_conta(numero)
        if conta is None:
            return False, "Conta nao encontrada."
        minimo = -conta["limite"] if conta["tipo"] == "corrente" else 0
        if conta["saldo"] - valor < minimo:
            return False, "Saldo insuficiente ou valor invalido!"
        with conectar() as conn:
            conn.execute(
                "UPDATE contas SET saldo = saldo - %s WHERE numero = %s",
                (Decimal(str(valor)), conta["numero"]),
            )
        return True, self.pegar_conta(numero)

    def render(self, numero):
        conta = self.pegar_conta(numero)
        if conta is None:
            return False, "Conta nao encontrada.", None
        if conta["tipo"] != "poupanca":
            return False, "Essa conta nao e poupanca.", None
        with conectar() as conn:
            row = conn.execute(
                "SELECT saldo, taxa_rendimento FROM contas WHERE numero = %s",
                (conta["numero"],),
            ).fetchone()
            rendimento = Decimal(row["saldo"]) * Decimal(row["taxa_rendimento"])
            conn.execute(
                "UPDATE contas SET saldo = saldo + %s WHERE numero = %s",
                (rendimento, conta["numero"]),
            )
        atualizada = self.pegar_conta(numero)
        return True, None, {"rendimento": float(rendimento), **atualizada}

    def excluir_conta(self, numero):
        conta = self.pegar_conta(numero)
        if conta is None:
            return False
        with conectar() as conn:
            conn.execute("DELETE FROM contas WHERE numero = %s", (conta["numero"],))
        return True
