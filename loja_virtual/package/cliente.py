class Cliente:
    def __init__(self, nome, email):
        self._nome = nome
        self._email = email

    def get_nome(self):
        return self._nome

    def get_email(self):
        return self._email

    def set_nome(self, nome):
        self._nome = nome

    def set_email(self, email):
        self._email = email

    def __str__(self):
        return f"{self._nome} ({self._email})"


class PessoaFisica:
    def __init__(self, cpf):
        self._cpf = cpf

    def get_cpf(self):
        return self._cpf

    def set_cpf(self, cpf):
        self._cpf = cpf


class PessoaJuridica:
    def __init__(self, cnpj):
        self._cnpj = cnpj

    def get_cnpj(self):
        return self._cnpj

    def set_cnpj(self, cnpj):
        self._cnpj = cnpj


class ClientePessoa(Cliente, PessoaFisica):
    def __init__(self, nome, email, cpf):
        Cliente.__init__(self, nome, email)
        PessoaFisica.__init__(self, cpf)

    def __str__(self):
        return f"{self._nome} (CPF: {self._cpf})"


class ClienteEmpresa(Cliente, PessoaJuridica):
    def __init__(self, nome, email, cnpj):
        Cliente.__init__(self, nome, email)
        PessoaJuridica.__init__(self, cnpj)

    def __str__(self):
        return f"{self._nome} (CNPJ: {self._cnpj})"
