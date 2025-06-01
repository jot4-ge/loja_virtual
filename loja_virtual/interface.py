import tkinter as tk
from tkinter import messagebox
from package.roupa import Roupa
from package.cliente import ClientePessoa
from package.pedido import Pedido

def iniciar_interface():
     catalogo = [
    Roupa(1, "Camisa Polo Lacoste", "Camisa importada da França", 350.00, 10, "M", "Branca", "Camisa"),
    Roupa(2, "Calça Jeans Levi's", "Original dos EUA", 420.00, 5, "42", "Azul", "Calça"),
    Roupa(3, "Casaco North Face", "Casaco térmico canadense", 980.00, 3, "G", "Preto", "Casaco"),
    Roupa(4, "Camiseta Supreme", "Exclusiva dos EUA", 550.00, 7, "M", "Preta", "Camiseta"),
    Roupa(5, "Jaqueta Adidas", "Importada da Alemanha", 610.00, 4, "G", "Verde", "Jaqueta"),
    Roupa(6, "Blusa Hering", "Blusa básica de algodão", 120.00, 12, "P", "Cinza", "Blusa"),
    Roupa(7, "Moletom GAP", "Moletom com capuz", 290.00, 8, "GG", "Azul", "Moletom"),
    Roupa(8, "Short Nike", "Short esportivo", 150.00, 15, "M", "Preto", "Short"),
    Roupa(9, "Camisa Xadrez Zara", "Estilo casual", 260.00, 6, "G", "Vermelha", "Camisa"),
    Roupa(10, "Saia Jeans", "Moda feminina", 200.00, 9, "38", "Azul", "Saia")
    ]

    cliente = None
    pedido = None

    def registrar_cliente():
        nonlocal cliente, pedido
        nome = entry_nome.get()
        email = entry_email.get()
        cpf = entry_cpf.get()
        if not nome or not email or not cpf:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        cliente = ClientePessoa(nome, email, cpf)
        pedido = Pedido(cliente)
        messagebox.showinfo("Sucesso", f"Cliente {nome} registrado com sucesso.")

    def mostrar_catalogo():
        output.config(state="normal")
        output.delete("1.0", tk.END)
        for produto in catalogo:
            output.insert(tk.END, f"{produto.get_id()}: {produto.get_nome()} - R${produto.get_preco():.2f} (Estoque: {produto.get_estoque()})\n")
        output.config(state="disabled")

    def adicionar_item():
        nonlocal pedido
        if not pedido:
            messagebox.showerror("Erro", "Registre o cliente primeiro.")
            return
        try:
            id_produto = int(entry_id.get())
            quantidade = int(entry_qtd.get())
            produto = next((p for p in catalogo if p.get_id() == id_produto), None)
            if produto:
                if produto.get_estoque() >= quantidade:
                    pedido.get_carrinho().adicionar_item(produto, quantidade)
                    produto.set_estoque(produto.get_estoque() - quantidade)
                    messagebox.showinfo("Sucesso", f"{quantidade}x {produto.get_nome()} adicionado(s) ao carrinho.")
                else:
                    messagebox.showerror("Erro", "Estoque insuficiente.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        except ValueError:
            messagebox.showerror("Erro", "ID e quantidade devem ser números.")

    def ver_carrinho():
        if not pedido:
            messagebox.showerror("Erro", "Registre o cliente primeiro.")
            return
        output.config(state="normal")
        output.delete("1.0", tk.END)
        itens = pedido.get_carrinho().get_itens()
        if not itens:
            output.insert(tk.END, "Carrinho vazio.\n")
        else:
            for item in itens:
                p = item["produto"]
                q = item["quantidade"]
                output.insert(tk.END, f"{p.get_nome()} - {q}x - R${p.get_preco() * q:.2f}\n")
            output.insert(tk.END, f"Total: R${pedido.get_carrinho().calcular_total():.2f}\n")
        output.config(state="disabled")

    def finalizar_pedido():
        if not pedido:
            messagebox.showerror("Erro", "Registre o cliente primeiro.")
            return
        if not pedido.get_carrinho().get_itens():
            messagebox.showwarning("Aviso", "Carrinho vazio. Adicione produtos antes.")
            return
        cpf_formatado = cliente.get_cpf().replace(".", "").replace("-", "")
        filename = f"pedido_{cpf_formatado}.json"
        pedido.salvar_em_json(filename)
        messagebox.showinfo("Pedido Finalizado", f"Pedido salvo como '{filename}'\n\n" + pedido.resumo_pedido())

    # Interface
    root = tk.Tk()
    root.title("Loja Virtual - Cadastro e Compras")

    cadastro_frame = tk.LabelFrame(root, text="Cadastro do Cliente")
    cadastro_frame.pack(padx=10, pady=10)

    tk.Label(cadastro_frame, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(cadastro_frame)
    entry_nome.grid(row=0, column=1)

    tk.Label(cadastro_frame, text="Email:").grid(row=1, column=0)
    entry_email = tk.Entry(cadastro_frame)
    entry_email.grid(row=1, column=1)

    tk.Label(cadastro_frame, text="CPF:").grid(row=2, column=0)
    entry_cpf = tk.Entry(cadastro_frame)
    entry_cpf.grid(row=2, column=1)

    tk.Button(cadastro_frame, text="Registrar Cliente", command=registrar_cliente).grid(row=3, column=0, columnspan=2, pady=5)

    compra_frame = tk.LabelFrame(root, text="Catálogo e Carrinho")
    compra_frame.pack(padx=10, pady=10)

    tk.Label(compra_frame, text="ID do Produto:").grid(row=0, column=0)
    entry_id = tk.Entry(compra_frame, width=5)
    entry_id.grid(row=0, column=1)

    tk.Label(compra_frame, text="Quantidade:").grid(row=0, column=2)
    entry_qtd = tk.Entry(compra_frame, width=5)
    entry_qtd.grid(row=0, column=3)

    tk.Button(compra_frame, text="Ver Catálogo", command=mostrar_catalogo).grid(row=1, column=0, pady=5)
    tk.Button(compra_frame, text="Adicionar ao Carrinho", command=adicionar_item).grid(row=1, column=1, pady=5)
    tk.Button(compra_frame, text="Ver Carrinho", command=ver_carrinho).grid(row=1, column=2, pady=5)
    tk.Button(compra_frame, text="Finalizar Pedido", command=finalizar_pedido).grid(row=1, column=3, pady=5)

    output = tk.Text(root, height=15, width=80, state="disabled")
    output.pack(pady=10)

    root.mainloop()

