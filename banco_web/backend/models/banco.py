# Guarda clientes e contas em memoria (igual ao banco_web).

from models.cliente import Cliente
from models.conta import ContaCorrente, ContaPoupanca


class Banco:
    def __init__(self):
        self.clientes = {}
        self.contas = {}
        self.proximo_numero = 1001

        ana = Cliente("Ana", "1")
        bruno = Cliente("Bruno", "2")
        self.clientes["1"] = ana
        self.clientes["2"] = bruno
        self.contas[1001] = ContaPoupanca(1001, ana, 1000)
        self.contas[1002] = ContaCorrente(1002, bruno, 100)
        self.proximo_numero = 1003

    def cadastrar_cliente(self, nome, cpf):
        if cpf in self.clientes:
            return None
        cliente = Cliente(nome, cpf)
        self.clientes[cpf] = cliente
        return cliente

    def criar_conta(self, cpf, tipo, saldo):
        cliente = self.clientes.get(cpf)
        if cliente is None:
            return None

        numero = self.proximo_numero
        self.proximo_numero += 1

        if tipo == "p":
            conta = ContaPoupanca(numero, cliente, saldo)
        else:
            conta = ContaCorrente(numero, cliente, saldo)

        self.contas[numero] = conta
        return conta

    def pegar_conta(self, numero):
        try:
            return self.contas.get(int(numero))
        except ValueError:
            return None

    def excluir_conta(self, numero):
        conta = self.pegar_conta(numero)
        if conta is None:
            return False
        del self.contas[conta.numero]
        return True
