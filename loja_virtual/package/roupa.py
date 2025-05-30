from .produto import Produto

class Roupa(Produto):
    def __init__(self, id, nome, descricao, preco, estoque, tamanho, cor, tipo):
        super().__init__(id, nome, descricao, preco, estoque)
        self.__tamanho = tamanho
        self.__cor = cor
        self.__tipo = tipo  # Ex: camiseta, calça, casaco

    def get_tamanho(self):
        return self.__tamanho

    def get_cor(self):
        return self.__cor

    def get_tipo(self):
        return self.__tipo

    def set_tamanho(self, tamanho):
        self.__tamanho = tamanho

    def set_cor(self, cor):
        self.__cor = cor

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def __str__(self):
        return (f"{self.get_nome()} ({self.__tipo}, Tamanho: {self.__tamanho}, Cor: {self.__cor}) - "
                f"R${self.get_preco():.2f} ({self.get_estoque()} em estoque)")
