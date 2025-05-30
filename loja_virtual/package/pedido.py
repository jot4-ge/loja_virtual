from .carrinho import Carrinho
import json

class Pedido:
    def __init__(self, cliente):
        self.__cliente = cliente
        self.__carrinho = Carrinho()
        self.__itens = self.__carrinho.get_itens()
        self.__total = self.__carrinho.calcular_total()

    def get_cliente(self):
        return self.__cliente

    def get_itens(self):
        return self.__itens

    def get_total(self):
        return self.__total

    def get_carrinho(self):
        return self.__carrinho

    def resumo_pedido(self):
        self.__itens = self.__carrinho.get_itens()
        self.__total = self.__carrinho.calcular_total()

        resumo = f"Cliente: {self.__cliente}\n"
        resumo += "Itens do pedido:\n"
        for item in self.__itens:
            produto = item["produto"]
            quantidade = item["quantidade"]
            subtotal = produto.get_preco() * quantidade
            resumo += f"- {produto.get_nome()} ({quantidade}x) - R${subtotal:.2f}\n"
        resumo += f"Total: R${self.__total:.2f}"
        return resumo

    def to_dict(self):
        return {
            "cliente": str(self.__cliente),
            "itens": [
                {
                    "nome": item["produto"].get_nome(),
                    "preco": item["produto"].get_preco(),
                    "quantidade": item["quantidade"],
                    "subtotal": item["produto"].get_preco() * item["quantidade"]
                } for item in self.__carrinho.get_itens()
            ],
            "total": self.__carrinho.calcular_total()
        }

    def salvar_em_json(self, nome_arquivo="pedido.json"):
        try:
            with open(nome_arquivo, "w", encoding="utf-8") as fjson:
                json.dump(self.to_dict(), fjson, indent=4, ensure_ascii=False)
            print(f"Pedido salvo em '{nome_arquivo}'.")
        except Exception as e:
            print(f"Erro ao salvar o pedido: {e}")

    @staticmethod
    def carregar_de_json(nome_arquivo="pedido.json"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as fjson:
                dados = json.load(fjson)
            return dados  # retorna dicionário com os dados do pedido
        except FileNotFoundError:
            print("Arquivo de pedido não encontrado.")
            return None


