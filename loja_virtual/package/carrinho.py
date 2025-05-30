class Carrinho:
    def __init__(self):
        self.__itens = []

    def adicionar_item(self, produto, quantidade):
        if produto.get_estoque() >= quantidade:
            for item in self.__itens:
                if item["produto"].get_id() == produto.get_id():
                    item["quantidade"] += quantidade
                    produto.set_estoque(produto.get_estoque() - quantidade)
                    return
            self.__itens.append({"produto": produto, "quantidade": quantidade})
            produto.set_estoque(produto.get_estoque() - quantidade)
        else:
            print(f"❌ Estoque insuficiente para {produto.get_nome()}.")

    def remover_item(self, produto_id):
        for item in self.__itens:
            if item["produto"].get_id() == produto_id:
                produto = item["produto"]
                produto.set_estoque(produto.get_estoque() + item["quantidade"])
                self.__itens.remove(item)
                return
        print("❌ Produto não encontrado no carrinho.")

    def get_itens(self):
        return self.__itens

    def calcular_total(self):
        total = 0
        for item in self.__itens:
            total += item["produto"].get_preco() * item["quantidade"]
        return total
