import mysql.connector
from mysql.connector import Error

# Função para conectar ao banco de dados
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123456789",
            database="estoque"
        )
        print("Conexão ao MySQL bem-sucedida")
        return connection
    except Error as e:
        print(f"O erro '{e}' ocorreu")
        return None

# Função para inserir produtos
def insert_product(connection):
    nome = input("Nome do produto: ")
    peso = float(input("Peso do produto: "))
    quantidade = int(input("Quantidade: "))
    quantidade_minima = int(input("Quantidade mínima: "))
    categoria_id = int(input("ID da categoria: "))

    cursor = connection.cursor()
    query = """
    INSERT INTO Produtos_Estoque (produto_nome, produto_peso, produto_quantidade, produto_quantidade_minima, categoria_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nome, peso, quantidade, quantidade_minima, categoria_id))
    connection.commit()
    print("Produto inserido com sucesso!")

def view_products(connection):
    cursor = connection.cursor()
    query = """
    SELECT p.produto_id, p.produto_nome, p.produto_peso, p.produto_quantidade, p.produto_quantidade_minima, c.categoria_nome AS categoria, f.fornecedor_nome AS fornecedor, pf.preco_fornecedor
    FROM Produtos_Estoque p
    JOIN Categorias_Produtos c ON p.categoria_id = c.categoria_id
    LEFT JOIN Relacao_Produto_Fornecedores pf ON p.produto_id = pf.produto_id
    LEFT JOIN Fornecedores f ON pf.fornecedor_id = f.fornecedor_id
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    for produto in produtos:
        print(
            f"ID: {produto[0]}, Nome: {produto[1]}, Peso: {produto[2]}, Quantidade: {produto[3]}, Quantidade Mínima: {produto[4]}, Categoria: {produto[5]}, Fornecedor: {produto[6]}, Preço do Fornecedor: {produto[7]}")

def view_low_stock_products(connection):
    cursor = connection.cursor()

    # Consulta para encontrar produtos com quantidade em estoque menor ou igual à quantidade mínima
    query = """
    SELECT produto_id, produto_nome, produto_quantidade, produto_quantidade_minima
    FROM Produtos_Estoque
    WHERE produto_quantidade <= produto_quantidade_minima
    ORDER BY produto_quantidade ASC
    """
    cursor.execute(query)
    produtos = cursor.fetchall()

    # Exibir os resultados
    if produtos:
        print("\nProdutos com quantidade em estoque menor ou igual à quantidade mínima requerida:")
        for produto in produtos:
            print(
                f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade em Estoque: {produto[2]}, Quantidade Mínima: {produto[3]}")
    else:
        print("\nTodos os produtos estão com quantidade em estoque acima da quantidade mínima requerida.")

# Função para criar Fornecedores
def insert_supplier(connection):
    nome = input("Nome do fornecedor: ")
    contato = input("Contato do fornecedor: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Fornecedores (fornecedor_nome, fornecedor_contato) 
    VALUES (%s, %s)
    """
    cursor.execute(query, (nome, contato))
    connection.commit()
    print("Fornecedor inserido com sucesso!")

def view_suppliers(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Fornecedores"
    cursor.execute(query)
    fornecedores = cursor.fetchall()

    for fornecedor in fornecedores:
        print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]}, Contato: {fornecedor[2]}")

def view_products_by_supplier(connection):
    fornecedor_id = int(input("Digite o ID do fornecedor para visualizar seus produtos: "))

    cursor = connection.cursor()
    query = """
    SELECT p.produto_id AS produto_id, p.produto_nome AS produto, p.produto_quantidade, p.produto_quantidade_minima, pf.preco_fornecedor
    FROM Relacao_Produto_Fornecedores pf
    JOIN Produtos_Estoque p ON pf.produto_id = p.produto_id
    WHERE pf.fornecedor_id = %s
    ORDER BY p.produto_nome
    """
    cursor.execute(query, (fornecedor_id,))
    produtos = cursor.fetchall()

    if produtos:
        print(f"\nProdutos do fornecedor ID {fornecedor_id}:")
        for produto in produtos:
            print(
                f"  ID Produto: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Quantidade Mínima: {produto[3]}, Preço do Fornecedor: {produto[4]}")
    else:
        print(f"Nenhum produto encontrado para o fornecedor ID {fornecedor_id}.")

# Função para criar Transportadoras
def insert_transporter(connection):
    nome = input("Nome da transportadora: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Transportadoras (transportadora_nome) 
    VALUES (%s)
    """
    cursor.execute(query, (nome,))
    connection.commit()
    print("Transportadora inserida com sucesso!")

def view_transporters(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Transportadoras"
    cursor.execute(query)
    transportadoras = cursor.fetchall()

    for transportadora in transportadoras:
        print(f"ID: {transportadora[0]}, Nome: {transportadora[1]}")

# Funções para criar Categorias_Produtos
def insert_category(connection):
    nome = input("Nome da categoria: ")

    cursor = connection.cursor()
    query = """
    INSERT INTO Categorias_Produtos (categoria_nome) 
    VALUES (%s)
    """
    cursor.execute(query, (nome,))
    connection.commit()
    print("Categoria inserida com sucesso!")

def view_categories(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM Categorias_Produtos"
    cursor.execute(query)
    categorias = cursor.fetchall()

    for categoria in categorias:
        print(f"ID: {categoria[0]}, Nome: {categoria[1]}")

def view_category_with_most_items(connection):
    cursor = connection.cursor()

    # Consulta para encontrar a categoria com mais itens no estoque
    query = """
    SELECT c.categoria_nome AS categoria, SUM(p.produto_quantidade) AS total_itens
    FROM Categorias_Produtos c
    JOIN Produtos_Estoque p ON c.categoria_id = p.categoria_id
    GROUP BY c.categoria_id
    ORDER BY total_itens DESC
    LIMIT 1
    """
    cursor.execute(query)
    resultado = cursor.fetchone()

    # Exibir o resultado
    if resultado:
        print(f"\nCategoria com mais itens em estoque: {resultado[0]} com {resultado[1]} itens")
    else:
        print("Nenhum item encontrado nas categorias.")

# Funções de Registro de Entrada e Saída
def register_product_entry(connection):
    produto_id = int(input("ID do produto: "))
    data_pedido = input("Data do pedido (AAAA-MM-DD): ")
    data_entrega = input("Data da entrega (AAAA-MM-DD): ")
    quantidade_entrada = int(input("Quantidade: "))
    peso_total_entrada = float(input("Peso total: "))
    transportadora_id = int(input("ID da transportadora: "))

    cursor = connection.cursor()
    query = """
    INSERT INTO Entradas_Estoque (produto_id, data_pedido, data_entrega, quantidade_entrada, peso_total_entrada, transportadora_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (produto_id, data_pedido, data_entrega, quantidade_entrada, peso_total_entrada, transportadora_id))
    connection.commit()
    print("Entrada registrada com sucesso!")

def register_product_exit(connection):
    data_saida = input("Data de saída (AAAA-MM-DD): ")
    loja_destino = input("Nome da loja: ")
    peso_total_saida = float(input("Peso total: "))
    transportadora_id = int(input("ID da transportadora: "))

    cursor = connection.cursor()
    query = """
    INSERT INTO Saidas_Estoque (data_saida, loja_destino, peso_total_saida, transportadora_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (data_saida, loja_destino, peso_total_saida, transportadora_id))
    saida_id = cursor.lastrowid

    while True:
        produto_id = int(input("ID do produto: "))
        quantidade_saida = int(input("Quantidade: "))
        preco_venda = float(input("Preço de venda: "))

        query = """
        INSERT INTO Relacao_Saida_Produtos (saida_id, produto_id, quantidade_saida, preco_venda)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (saida_id, produto_id, quantidade_saida, preco_venda))

        more = input("Adicionar mais produtos a esta saída? (s/n): ")
        if more.lower() != 's':
            break

    connection.commit()
    print("Saída registrada com sucesso!")

# Visualização de Entradas e Saídas
def view_entries(connection):
    cursor = connection.cursor()
    produto_id = int(input("Digite o ID do produto para visualizar as entradas: "))
    query = """
    SELECT e.entrada_id, p.produto_nome AS produto, e.data_pedido, e.data_entrega, e.quantidade_entrada, e.peso_total_entrada, t.transportadora_nome AS transportadora,
           DATEDIFF(e.data_entrega, e.data_pedido) AS tempo_entrega
    FROM Entradas_Estoque e
    JOIN Produtos_Estoque p ON e.produto_id = p.produto_id
    JOIN Transportadoras t ON e.transportadora_id = t.transportadora_id
    WHERE e.produto_id = %s
    ORDER BY e.data_entrega ASC
    """
    cursor.execute(query, (produto_id,))
    entradas = cursor.fetchall()

    for entrada in entradas:
        print(
            f"ID: {entrada[0]}, Produto: {entrada[1]}, Data do Pedido: {entrada[2]}, Data de Entrega: {entrada[3]}, Tempo de Entrega: {entrada[4]} dias, Quantidade: {entrada[5]}, Peso Total: {entrada[6]}, Transportadora: {entrada[7]}")


def view_exits(connection):
    cursor = connection.cursor()
    produto_id = int(input("Digite o ID do produto para visualizar as saídas: "))
    query = """
    SELECT s.saida_id, sp.produto_id, p.produto_nome AS produto, sp.quantidade_saida, sp.preco_venda, s.data_saida, s.loja_destino, s.peso_total_saida, t.transportadora_nome AS transportadora
    FROM Saidas_Estoque s
    JOIN Relacao_Saida_Produtos sp ON s.saida_id = sp.saida_id
    JOIN Produtos_Estoque p ON sp.produto_id = p.produto_id
    JOIN Transportadoras t ON s.transportadora_id = t.transportadora_id
    WHERE sp.produto_id = %s
    ORDER BY s.data_saida ASC
    """
    cursor.execute(query, (produto_id,))
    saidas = cursor.fetchall()

    for saida in saidas:
        print(
            f"ID: {saida[0]}, Produto: {saida[2]}, Quantidade: {saida[3]}, Preço de Venda: {saida[4]}, Data de Saída: {saida[5]}, Loja: {saida[6]}, Peso Total: {saida[7]}, Transportadora: {saida[8]}")

# Visualização de Histórico Completo de Produto
def view_product_history(connection):
    produto_id = int(input("Digite o ID do produto para visualizar o histórico completo: "))

    cursor = connection.cursor()

    # Consultar Entradas do Produto
    query_entradas = """
    SELECT e.data_pedido, e.data_entrega, e.quantidade_entrada, e.peso_total_entrada, t.transportadora_nome AS transportadora,
           DATEDIFF(e.data_entrega, e.data_pedido) AS tempo_entrega
    FROM Entradas_Estoque e
    JOIN Transportadoras t ON e.transportadora_id = t.transportadora_id
    WHERE e.produto_id = %s
    ORDER BY e.data_entrega ASC
    """
    cursor.execute(query_entradas, (produto_id,))
    entradas = cursor.fetchall()

    # Consultar Saídas do Produto
    query_saidas = """
    SELECT s.data_saida, sp.quantidade_saida, sp.preco_venda, s.loja_destino, s.peso_total_saida, t.transportadora_nome AS transportadora
    FROM Saidas_Estoque s
    JOIN Relacao_Saida_Produtos sp ON s.saida_id = sp.saida_id
    JOIN Transportadoras t ON s.transportadora_id = t.transportadora_id
    WHERE sp.produto_id = %s
    ORDER BY s.data_saida ASC
    """
    cursor.execute(query_saidas, (produto_id,))
    saidas = cursor.fetchall()

    # Exibir Histórico
    print(f"\nHistórico completo do Produto ID {produto_id}:")
    print("\nEntradas:")
    if entradas:
        for entrada in entradas:
            print(
                f"  Data do Pedido: {entrada[0]}, Data de Entrega: {entrada[1]}, Tempo de Entrega: {entrada[5]} dias, Quantidade: {entrada[2]}, Peso Total: {entrada[3]}, Transportadora: {entrada[4]}")
    else:
        print("  Nenhuma entrada registrada.")

    print("\nSaídas:")
    if saidas:
        for saida in saidas:
            print(
                f"  Data de Saída: {saida[0]}, Quantidade: {saida[1]}, Preço de Venda: {saida[2]}, Loja: {saida[3]}, Peso Total: {saida[4]}, Transportadora: {saida[5]}")
    else:
        print("  Nenhuma saída registrada.")

# Função para calcular o faturamento por loja
def calculate_revenue_by_store(connection):
    month = input("Digite o mês para calcular o faturamento (formato MM): ")
    year = input("Digite o ano para calcular o faturamento (formato YYYY): ")

    cursor = connection.cursor()

    # Consulta para calcular o faturamento total por loja
    query = """
    SELECT s.loja_destino, SUM(sp.quantidade_saida * sp.preco_venda) AS total_vendas
    FROM Saidas_Estoque s
    JOIN Relacao_Saida_Produtos sp ON s.saida_id = sp.saida_id
    WHERE MONTH(s.data_saida) = %s AND YEAR(s.data_saida) = %s
    GROUP BY s.loja_destino
    ORDER BY total_vendas DESC
    """
    cursor.execute(query, (month, year))
    resultados = cursor.fetchall()

    # Exibir os resultados
    if resultados:
        print(f"\nFaturamento por loja no mês {month}/{year}:")
        for loja, total_vendas in resultados:
            print(f"Loja: {loja}, Faturamento: R${total_vendas:.2f}")

        # Identificar a loja com maior faturamento
        loja_mais_vendas = resultados[0]
        print(f"\nLoja com maior faturamento: {loja_mais_vendas[0]} com R${loja_mais_vendas[1]:.2f}")
    else:
        print(f"Nenhuma venda registrada no mês {month}/{year}.")

# Menu interativo
def main_menu():
    print("\nMenu Principal")
    print("1. Gerenciar Produtos")
    print("2. Gerenciar Fornecedores")
    print("3. Gerenciar Transportadoras")
    print("4. Gerenciar Categorias")
    print("5. Registrar Entrada de Produto")
    print("6. Registrar Saída de Produto")
    print("7. Visualizar Entradas")
    print("8. Visualizar Saídas")
    print("9. Visualizar Histórico de Produto")
    print("10. Calcular Faturamento por Loja")
    print("11. Sair")

def product_menu():
    print("\nMenu de Produtos")
    print("1. Inserir novo produto")
    print("2. Visualizar todos os produtos")
    print("3. Visualizar produtos com estoque baixo")
    print("4. Voltar ao Menu Principal")

def supplier_menu():
    print("\nMenu de Fornecedores")
    print("1. Inserir novo fornecedor")
    print("2. Visualizar todos os fornecedores")
    print("3. Visualizar produtos por fornecedor")
    print("4. Voltar ao Menu Principal")

def transporter_menu():
    print("\nMenu de Transportadoras")
    print("1. Inserir nova transportadora")
    print("2. Visualizar todas as transportadoras")
    print("3. Voltar ao Menu Principal")

def category_menu():
    print("\nMenu de Categorias")
    print("1. Inserir nova categoria")
    print("2. Visualizar todas as categorias")
    print("3. Ver categoria com mais itens em estoque")
    print("4. Voltar ao Menu Principal")

def main():
    connection = create_connection()
    if connection is None:
        return

    while True:
        main_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            while True:
                product_menu()
                product_choice = input("Escolha uma opção: ")
                if product_choice == '1':
                    insert_product(connection)
                elif product_choice == '2':
                    view_products(connection)
                elif product_choice == '3':
                    view_low_stock_products(connection)
                elif product_choice == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '2':
            while True:
                supplier_menu()
                supplier_choice = input("Escolha uma opção: ")
                if supplier_choice == '1':
                    insert_supplier(connection)
                elif supplier_choice == '2':
                    view_suppliers(connection)
                elif supplier_choice == '3':
                    view_products_by_supplier(connection)
                elif supplier_choice == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '3':
            while True:
                transporter_menu()
                transporter_choice = input("Escolha uma opção: ")
                if transporter_choice == '1':
                    insert_transporter(connection)
                elif transporter_choice == '2':
                    view_transporters(connection)
                elif transporter_choice == '3':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '4':
            while True:
                category_menu()
                category_choice = input("Escolha uma opção: ")
                if category_choice == '1':
                    insert_category(connection)
                elif category_choice == '2':
                    view_categories(connection)
                elif category_choice == '3':
                    view_category_with_most_items(connection)
                elif category_choice == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")

        elif choice == '5':
            register_product_entry(connection)

        elif choice == '6':
            register_product_exit(connection)

        elif choice == '7':
            view_entries(connection)

        elif choice == '8':
            view_exits(connection)

        elif choice == '9':
            view_product_history(connection)

        elif choice == '10':
            calculate_revenue_by_store(connection)

        elif choice == '11':
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    connection.close()

if __name__ == "__main__":
    main()
