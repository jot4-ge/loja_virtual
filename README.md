# Loja Virtual - Projeto Livre de Programação Orientada a Objetos

Desenvolvido como Projeto Livre na disciplina de Programação Orientada a Objetos, este sistema simula uma loja virtual com catálogo de roupas, carrinho de compras, controle de estoque e finalização de pedidos. O projeto foi construído utilizando Python com foco em boas práticas de orientação a objetos e interface gráfica com Tkinter.

## Demonstração do projeto

O sistema pode ser executado em ambiente local e conta com uma interface gráfica simples e funcional. O diagrama de classes também está incluído para demonstrar a modelagem orientada a objetos.

## Como rodar

Certifique-se de ter o Python 3 instalado. Em seguida:

1. Clone este repositório ou baixe os arquivos.
2. Navegue até a pasta do projeto no terminal:
   ```bash
   cd loja_virtual
Execute o sistema com:

bash
Copiar
Editar
python main.py

## Casos de Uso

### 1. Cadastro de Cliente
- O usuário insere seu nome, e-mail e CPF.
- O sistema valida os dados e cria uma instância do cliente.
- O pedido é automaticamente associado a esse cliente.

### 2. Visualização do Catálogo
- O usuário pode visualizar os produtos disponíveis diretamente na interface.
- São exibidas informações como: nome, descrição, preço, estoque, tamanho, cor e categoria.

### 3. Adicionar Produto ao Carrinho
- O usuário escolhe um produto pelo ID e informa a quantidade desejada.
- O sistema verifica se há estoque suficiente.
- Se validado, o item é adicionado ao carrinho e o estoque do produto é reduzido imediatamente.

### 4. Ver Carrinho
- Exibe todos os itens adicionados ao carrinho, com nome do produto, quantidade e subtotal.
- O total acumulado do pedido é calculado automaticamente e exibido ao usuário.

### 5. Finalizar Pedido
- Após revisar os itens no carrinho, o usuário pode finalizar a compra.
- O sistema gera um resumo do pedido e salva os dados automaticamente em um arquivo JSON nomeado com o CPF do cliente (ex: `pedido_12345678900.json`).
- Isso garante rastreabilidade e persistência de dados mesmo após o fechamento da aplicação.

### 6. Interface Gráfica
- A aplicação conta com uma interface criada com Tkinter.
- Os botões e campos permitem interação intuitiva com o sistema: cadastrar cliente, adicionar produto, ver carrinho e finalizar pedido.




### Tecnologias Utilizadas
- Python 3

- Tkinter (interface gráfica)

- Programação Orientada a Objetos

- Serialização de dados com JSON

- Diagrama de Classes

