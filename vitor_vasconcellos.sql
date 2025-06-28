CREATE TABLE Fornecedores (
    fornecedor_id INT AUTO_INCREMENT PRIMARY KEY,
    fornecedor_nome VARCHAR(255) NOT NULL,
    fornecedor_contato VARCHAR(255)
);

CREATE TABLE Categorias_Produtos (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_nome VARCHAR(255) NOT NULL
);

CREATE TABLE Produtos_Estoque (
    produto_id INT AUTO_INCREMENT PRIMARY KEY,
    produto_nome VARCHAR(255) NOT NULL,
    produto_peso FLOAT(5,2) NOT NULL,
    produto_quantidade INT NOT NULL,
    produto_quantidade_minima INT NOT NULL,
    categoria_id INT NOT NULL
);

CREATE TABLE Relacao_Produto_Fornecedores (
    relacao_id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    fornecedor_id INT NOT NULL,
    preco_fornecedor FLOAT(10, 2) NOT NULL
);

CREATE TABLE Transportadoras (
    transportadora_id INT AUTO_INCREMENT PRIMARY KEY,
    transportadora_nome VARCHAR(255) NOT NULL
);

CREATE TABLE Entradas_Estoque (
    entrada_id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    data_pedido DATE,
    data_entrega DATE,
    quantidade_entrada INT,
    peso_total_entrada FLOAT(10, 2),
    transportadora_id INT
);

CREATE TABLE Saidas_Estoque (
    saida_id INT AUTO_INCREMENT PRIMARY KEY,
    data_saida DATE,
    loja_destino VARCHAR(255),
    peso_total_saida FLOAT(10, 2),
    transportadora_id INT
);

CREATE TABLE Relacao_Saida_Produtos (
    relacao_saida_id INT AUTO_INCREMENT PRIMARY KEY,
    saida_id INT NOT NULL,
    produto_id INT NOT NULL,
    quantidade_saida INT NOT NULL,
    preco_venda FLOAT(10, 2) NOT NULL
);

//

ALTER TABLE Produtos_Estoque
ADD CONSTRAINT fk_categoria_produto
FOREIGN KEY (categoria_id)
REFERENCES Categorias_Produtos(categoria_id);

ALTER TABLE Relacao_Produto_Fornecedores
ADD CONSTRAINT fk_relacao_produto_fornecedor_produto
FOREIGN KEY (produto_id)
REFERENCES Produtos_Estoque(produto_id);

ALTER TABLE Relacao_Produto_Fornecedores
ADD CONSTRAINT fk_relacao_produto_fornecedor_fornecedor
FOREIGN KEY (fornecedor_id)
REFERENCES Fornecedores(fornecedor_id);

ALTER TABLE Entradas_Estoque
ADD CONSTRAINT fk_entrada_produto
FOREIGN KEY (produto_id)
REFERENCES Produtos_Estoque(produto_id);

ALTER TABLE Entradas_Estoque
ADD CONSTRAINT fk_entrada_transportadora
FOREIGN KEY (transportadora_id)
REFERENCES Transportadoras(transportadora_id);

ALTER TABLE Saidas_Estoque
ADD CONSTRAINT fk_saida_transportadora
FOREIGN KEY (transportadora_id)
REFERENCES Transportadoras(transportadora_id);

ALTER TABLE Relacao_Saida_Produtos
ADD CONSTRAINT fk_saida_produto_saida
FOREIGN KEY (saida_id)
REFERENCES Saidas_Estoque(saida_id);

ALTER TABLE Relacao_Saida_Produtos
ADD CONSTRAINT fk_saida_produto_produto
FOREIGN KEY (produto_id)
REFERENCES Produtos_Estoque(produto_id);

//

POPULANDO O BANCO

-- Inserindo dados na tabela Fornecedores
INSERT INTO Fornecedores (fornecedor_nome, fornecedor_contato) VALUES
('Fornecedor A', 'contatoA@fornecedor.com'),
('Fornecedor B', 'contatoB@fornecedor.com'),
('Fornecedor C', 'contatoC@fornecedor.com');

-- Inserindo dados na tabela Categorias_Produtos
INSERT INTO Categorias_Produtos (categoria_nome) VALUES
('Eletrônicos'),
('Móveis'),
('Alimentos');

-- Inserindo dados na tabela Produtos_Estoque
INSERT INTO Produtos_Estoque (produto_nome, produto_peso, produto_quantidade, produto_quantidade_minima, categoria_id) VALUES
('Televisão', 10.5, 50, 10, 1),  -- Eletrônicos
('Sofá', 30.0, 20, 5, 2),        -- Móveis
('Arroz', 1.0, 100, 20, 3);       -- Alimentos

-- Inserindo dados na tabela Relacao_Produto_Fornecedores
INSERT INTO Relacao_Produto_Fornecedores (produto_id, fornecedor_id, preco_fornecedor) VALUES
(1, 1, 1500.00),  -- Televisão de Fornecedor A
(2, 2, 500.00),   -- Sofá de Fornecedor B
(3, 3, 25.00);    -- Arroz de Fornecedor C

-- Inserindo dados na tabela Transportadoras
INSERT INTO Transportadoras (transportadora_nome) VALUES
('Transportadora X'),
('Transportadora Y');

-- Inserindo dados na tabela Entradas_Estoque
INSERT INTO Entradas_Estoque (produto_id, data_pedido, data_entrega, quantidade_entrada, peso_total_entrada, transportadora_id) VALUES
(1, '2024-08-01', '2024-08-03', 20, 210.0, 1),  -- 20 televisões entregues pela Transportadora X
(2, '2024-08-02', '2024-08-04', 5, 150.0, 2);   -- 5 sofás entregues pela Transportadora Y

-- Inserindo dados na tabela Saidas_Estoque
INSERT INTO Saidas_Estoque (data_saida, loja_destino, peso_total_saida, transportadora_id) VALUES
('2024-08-05', 'Loja A', 105.0, 1),  -- Entrega para Loja A pela Transportadora X
('2024-08-06', 'Loja B', 150.0, 2);  -- Entrega para Loja B pela Transportadora Y

-- Inserindo dados na tabela Relacao_Saida_Produtos
INSERT INTO Relacao_Saida_Produtos (saida_id, produto_id, quantidade_saida, preco_venda) VALUES
(1, 1, 10, 2000.00),  -- 10 televisões vendidas para Loja A
(2, 2, 3, 750.00);    -- 3 sofás vendidos para Loja B

-- Inserindo mais dados na tabela Produtos_Estoque
INSERT INTO Produtos_Estoque (produto_nome, produto_peso, produto_quantidade, produto_quantidade_minima, categoria_id) VALUES
('Geladeira', 60.0, 15, 3, 1),  -- Eletrônicos
('Mesa', 25.0, 10, 3, 2),       -- Móveis
('Feijão', 1.0, 80, 15, 3);     -- Alimentos

-- Inserindo mais dados na tabela Relacao_Produto_Fornecedores
INSERT INTO Relacao_Produto_Fornecedores (produto_id, fornecedor_id, preco_fornecedor) VALUES
(4, 1, 2500.00),  -- Geladeira de Fornecedor A
(5, 2, 300.00),   -- Mesa de Fornecedor B
(6, 3, 15.00);    -- Feijão de Fornecedor C

-- Inserindo mais dados na tabela Entradas_Estoque
INSERT INTO Entradas_Estoque (produto_id, data_pedido, data_entrega, quantidade_entrada, peso_total_entrada, transportadora_id) VALUES
(3, '2024-08-03', '2024-08-05', 50, 50.0, 1),   -- 50 unidades de Arroz entregues pela Transportadora X
(4, '2024-08-04', '2024-08-06', 5, 300.0, 2);   -- 5 Geladeiras entregues pela Transportadora Y

-- Inserindo mais dados na tabela Saidas_Estoque
INSERT INTO Saidas_Estoque (data_saida, loja_destino, peso_total_saida, transportadora_id) VALUES
('2024-08-07', 'Loja C', 75.0, 1),  -- Entrega para Loja C pela Transportadora X
('2024-08-08', 'Loja D', 300.0, 2); -- Entrega para Loja D pela Transportadora Y

-- Inserindo mais dados na tabela Relacao_Saida_Produtos
INSERT INTO Relacao_Saida_Produtos (saida_id, produto_id, quantidade_saida, preco_venda) VALUES
(1, 3, 30, 30.00),  -- 30 unidades de Arroz vendidas para Loja A
(2, 4, 2, 3200.00); -- 2 Geladeiras vendidas para Loja B
