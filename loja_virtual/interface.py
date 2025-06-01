import tkinter as tk
from tkinter import messagebox
import re
import json
import os
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

    # Arquivo para salvar cadastro
    arquivo_cadastro = "cadastro_lembrado.json"

    def salvar_cadastro(nome, email, cpf):
        dados = {"nome": nome, "email": email, "cpf": cpf}
        with open(arquivo_cadastro, "w") as f:
            json.dump(dados, f)

    def carregar_cadastro():
        if os.path.exists(arquivo_cadastro):
            with open(arquivo_cadastro, "r") as f:
                dados = json.load(f)
                return dados.get("nome", ""), dados.get("email", ""), dados.get("cpf", "")
        return "", "", ""

    def validar_email(email):
        # Regex simples para validar email
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(regex, email) is not None

    def validar_nome(nome):
        # Nome só letras (maiúsculas/minúsculas) e espaços
        return all(c.isalpha() or c.isspace() for c in nome) and len(nome) > 0

    def registrar_cliente():
        nonlocal cliente, pedido
        nome = entry_nome.get().strip()
        email = entry_email.get().strip()
        cpf = entry_cpf.get().strip()

        if not nome or not email or not cpf:
            messagebox.showerror("Campos obrigatórios", "Preencha nome, e-mail e CPF.")
            return

        if not validar_nome(nome):
            messagebox.showerror("Nome inválido", "O nome deve conter apenas letras e espaços.")
            return

        if not validar_email(email):
            messagebox.showerror("Email inválido", "Digite um endereço de e-mail válido.")
            return

        if not cpf.isdigit() or len(cpf) != 11:
            messagebox.showerror("CPF inválido", "O CPF deve conter exatamente 11 dígitos numéricos.")
            return

        cliente = ClientePessoa(nome, email, cpf)
        pedido = Pedido(cliente)
        messagebox.showinfo("Sucesso", f"Cliente {nome} registrado com sucesso.")

        if var_lembrar.get():
            salvar_cadastro(nome, email, cpf)
        else:
            # Se não quiser lembrar, apaga arquivo se existir
            if os.path.exists(arquivo_cadastro):
                os.remove(arquivo_cadastro)

    def mostrar_catalogo():
        output.config(state="normal")
        output.delete("1.0", tk.END)
        for produto in catalogo:
            output.insert(tk.END, f"{produto.get_id()}: {produto.get_nome()} - R${produto.get_preco():.2f} (Estoque: {produto.get_estoque()})\n")
        output.config(state="disabled")

    def adicionar_item():
        nonlocal pedido
        if not pedido:
            messagebox.showerror("Cliente não registrado", "Você precisa registrar um cliente antes de continuar.")
            return
        try:
            id_produto = int(entry_id.get())
            quantidade = int(entry_qtd.get())
            if quantidade <= 0:
                messagebox.showerror("Quantidade inválida", "A quantidade deve ser maior que zero.")
                return

            produto = next((p for p in catalogo if p.get_id() == id_produto), None)
            if produto:
                if produto.get_estoque() >= quantidade:
                    pedido.get_carrinho().adicionar_item(produto, quantidade)
                    produto.set_estoque(produto.get_estoque() - quantidade)
                    messagebox.showinfo("Sucesso", f"{quantidade}x {produto.get_nome()} adicionado(s) ao carrinho.")
                    entry_id.delete(0, tk.END)
                    entry_qtd.delete(0, tk.END)
                else:
                    messagebox.showerror("Estoque insuficiente", "A quantidade solicitada excede o estoque disponível.")
            else:
                messagebox.showerror("Produto não encontrado", "O ID informado não corresponde a nenhum produto.")
        except ValueError:
            messagebox.showerror("Entrada inválida", "ID e quantidade devem ser números inteiros.")

    def ver_carrinho():
        if not pedido:
            messagebox.showerror("Cliente não registrado", "Você precisa registrar um cliente antes de continuar.")
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
        nonlocal cliente, pedido
        if not pedido:
            messagebox.showerror("Cliente não registrado", "Você precisa registrar um cliente antes de continuar.")
            return
        if not pedido.get_carrinho().get_itens():
            messagebox.showwarning("Carrinho vazio", "Adicione produtos antes de finalizar o pedido.")
            return
        cpf_formatado = cliente.get_cpf().replace(".", "").replace("-", "")
        filename = f"pedido_{cpf_formatado}.json"
        pedido.salvar_em_json(filename)
        messagebox.showinfo("Pedido Finalizado", f"Pedido salvo como '{filename}'\n\n" + pedido.resumo_pedido())

        # Reset interface
        entry_id.delete(0, tk.END)
        entry_qtd.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        var_lembrar.set(0)
        output.config(state="normal")
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Pedido finalizado com sucesso. Inicie um novo cadastro para continuar.")
        output.config(state="disabled")
        cliente = None
        pedido = None

    # Interface
    root = tk.Tk()
    root.title("Loja Virtual - Cadastro e Compras")

    # Definir tamanho fixo da janela e centralizar
    largura = 900
    altura = 600
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = int(largura_tela/2 - largura/2)
    pos_y = int(altura_tela/2 - altura/2)
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    root.resizable(False, False)  # impede redimensionamento

    # Fontes padrão
    fonte = ("Arial", 10)

    cadastro_frame = tk.LabelFrame(root, text="Cadastro do Cliente", font=fonte)
    cadastro_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(cadastro_frame, text="Nome:", font=fonte).grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(cadastro_frame, font=fonte)
    entry_nome.grid(row=0, column=1, padx=5, pady=2, sticky="w")

    tk.Label(cadastro_frame, text="Email:", font=fonte).grid(row=1, column=0, sticky="w")
    entry_email = tk.Entry(cadastro_frame, font=fonte)
    entry_email.grid(row=1, column=1, padx=5, pady=2, sticky="w")

    tk.Label(cadastro_frame, text="CPF:", font=fonte).grid(row=2, column=0, sticky="w")
    entry_cpf = tk.Entry(cadastro_frame, font=fonte)
    entry_cpf.grid(row=2, column=1, padx=5, pady=2, sticky="w")

    var_lembrar = tk.IntVar()
    chk_lembrar = tk.Checkbutton(cadastro_frame, text="Lembrar cadastro", variable=var_lembrar, font=fonte)
    chk_lembrar.grid(row=3, column=0, columnspan=2, sticky="w", padx=5)

    tk.Button(cadastro_frame, text="Registrar Cliente", command=registrar_cliente, font=fonte).grid(row=4, column=0, columnspan=2, pady=5)

    compra_frame = tk.LabelFrame(root, text="Catálogo e Carrinho", font=fonte)
    compra_frame.pack(padx=10, pady=10, fill="x")

    tk.Label(compra_frame, text="ID do Produto:", font=fonte).grid(row=0, column=0, sticky="w")
    entry_id = tk.Entry(compra_frame, width=5, font=fonte)
    entry_id.grid(row=0, column=1, padx=5, pady=2, sticky="w")

    tk.Label(compra_frame, text="Quantidade:", font=fonte).grid(row=0, column=2, sticky="w")
    entry_qtd = tk.Entry(compra_frame, width=5, font=fonte)
    entry_qtd.grid(row=0, column=3, padx=5, pady=2, sticky="w")

    tk.Button(compra_frame, text="Ver Catálogo", command=mostrar_catalogo, font=fonte).grid(row=1, column=0, pady=5)
    tk.Button(compra_frame, text="Adicionar ao Carrinho", command=adicionar_item, font=fonte).grid(row=1, column=1, pady=5)
    tk.Button(compra_frame, text="Ver Carrinho", command=ver_carrinho, font=fonte).grid(row=1, column=2, pady=5)
    tk.Button(compra_frame, text="Finalizar Pedido", command=finalizar_pedido, font=fonte).grid(row=1, column=3, pady=5)

    output = tk.Text(root, height=15, width=80, state="disabled", font=fonte)
    output.pack(pady=10)

    # Ao iniciar, tentar carregar cadastro salvo
    nome_salvo, email_salvo, cpf_salvo = carregar_cadastro()
    if nome_salvo or email_salvo or cpf_salvo:
        entry_nome.insert(0, nome_salvo)
        entry_email.insert(0, email_salvo)
        entry_cpf.insert(0, cpf_salvo)
        var_lembrar.set(1)

    root.mainloop()



