# Regras da conta. Sem print: a API devolve JSON.


class Conta:
    def __init__(self, numero, titular, saldo):
        self.numero = numero
        self.titular = titular
        self._saldo = saldo

    def saldo(self):
        return self._saldo

    def resumo(self):
        return (
            f"Conta {self.numero} | Titular: {self.titular.nome} | "
            f"Saldo: R$ {self._saldo:.2f}"
        )

    def depositar(self, valor):
        if valor <= 0:
            return False
        self._saldo += valor
        return True

    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            return True
        return False


class ContaPoupanca(Conta):
    def __init__(self, numero, titular, saldo, taxa_rendimento=0.01):
        super().__init__(numero, titular, saldo)
        self.taxa_rendimento = taxa_rendimento

    def render(self):
        rendimento = self._saldo * self.taxa_rendimento
        self._saldo += rendimento
        return rendimento


class ContaCorrente(Conta):
    def __init__(self, numero, titular, saldo, limite=200.0):
        super().__init__(numero, titular, saldo)
        self.limite = limite

    def sacar(self, valor):
        if valor > 0 and (self._saldo - valor) >= -self.limite:
            self._saldo -= valor
            return True
        return False
