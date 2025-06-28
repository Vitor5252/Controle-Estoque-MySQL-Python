# 📦 Sistema de Controle de Estoque

Projeto desenvolvido para gerenciar o estoque de um centro de distribuição, com funcionalidades completas de cadastro, movimentação e consulta de dados. Utiliza **Python** para a lógica de negócio e **MySQL** como banco de dados.

## 🚀 Funcionalidades

- Cadastro de produtos, fornecedores, categorias e transportadoras
- Registro de entradas e saídas de estoque
- Visualização de produtos com estoque abaixo do mínimo
- Histórico completo de movimentação por produto
- Cálculo de faturamento mensal por loja
- Consultas SQL personalizadas e interativas via terminal

## 🧱 Tecnologias Utilizadas

- Python 3
- MySQL
- Conector MySQL para Python (`mysql-connector-python`)

## 🗂️ Organização do Projeto

- `vitor_vasconcellos.py` → código principal em Python
- `vitor_vasconcellos.sql` → estrutura do banco de dados + dados populados
- `ControleEstoque.pdf` → documento com os requisitos do sistema
- `vitor-vasconcellos-diagrama.png` → diagrama ER (relacional ou UML)

## 📌 Requisitos

- Python 3 instalado
- MySQL em execução local (`user=root`, `senha=123456789`)
- Executar o script SQL antes de rodar o programa

## ▶️ Como executar

1. Instale as dependências:
   ```bash
   pip install mysql-connector-python
