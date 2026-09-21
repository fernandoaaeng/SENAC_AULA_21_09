# PostgreSQL. As senhas do seed sao fracas de proposito (aula de laboratorio).

import os
import time
from contextlib import contextmanager
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_PATH = DATA_DIR / "acessos.log"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nexus:nexus@localhost:5432/nexusbank",
)

# VULNERAVEL DE PROPOSITO: credenciais fracas e conhecidas no seed.
SEED_USUARIOS = [
    ("ana", "123456", "cliente", "1"),
    ("bruno", "senha123", "cliente", "2"),
    ("carlos", "qwerty", "cliente", None),
    ("operador", "op123", "operador", None),
    ("admin", "admin123", "admin", None),
]


@contextmanager
def conectar():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def iniciar_banco():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("", encoding="utf-8")

    ultimo_erro = None
    for _ in range(30):
        try:
            _criar_esquema()
            return
        except Exception as erro:
            ultimo_erro = erro
            time.sleep(1)
    raise ultimo_erro


def _criar_esquema():
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                cpf TEXT PRIMARY KEY,
                nome TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                papel TEXT NOT NULL DEFAULT 'cliente',
                cliente_cpf TEXT REFERENCES clientes(cpf)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contas (
                numero INTEGER PRIMARY KEY,
                cliente_cpf TEXT NOT NULL REFERENCES clientes(cpf),
                tipo TEXT NOT NULL,
                saldo NUMERIC(14, 2) NOT NULL DEFAULT 0,
                limite NUMERIC(14, 2) NOT NULL DEFAULT 200,
                taxa_rendimento NUMERIC(8, 4) NOT NULL DEFAULT 0.01
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS logs_acesso (
                id SERIAL PRIMARY KEY,
                usuario TEXT NOT NULL,
                sucesso INTEGER NOT NULL,
                ip TEXT,
                criado_em TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessoes (
                token TEXT PRIMARY KEY,
                usuario TEXT NOT NULL,
                papel TEXT NOT NULL,
                ip TEXT,
                criado_em TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE SEQUENCE IF NOT EXISTS contas_numero_seq
            START WITH 1001 INCREMENT BY 1
            """
        )

        conn.execute(
            """
            INSERT INTO clientes (cpf, nome)
            VALUES ('1', 'Ana'), ('2', 'Bruno')
            ON CONFLICT (cpf) DO NOTHING
            """
        )
        for usuario, senha, papel, cliente_cpf in SEED_USUARIOS:
            # VULNERAVEL DE PROPOSITO: senha guardada em texto puro, sem hash.
            conn.execute(
                """
                INSERT INTO usuarios (usuario, senha, papel, cliente_cpf)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (usuario) DO NOTHING
                """,
                (usuario, senha, papel, cliente_cpf),
            )
        conn.execute(
            """
            INSERT INTO contas (numero, cliente_cpf, tipo, saldo, limite, taxa_rendimento)
            VALUES
                (1001, '1', 'poupanca', 1000, 0, 0.01),
                (1002, '2', 'corrente', 100, 200, 0)
            ON CONFLICT (numero) DO NOTHING
            """
        )
        conn.execute(
            """
            SELECT setval(
                'contas_numero_seq',
                GREATEST((SELECT COALESCE(MAX(numero), 1000) FROM contas), 1000)
            )
            """
        )
