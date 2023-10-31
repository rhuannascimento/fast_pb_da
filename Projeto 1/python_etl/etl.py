import pymongo
import psycopg2
import csv

#informações do mongo DB
mongo_host = "mongodb"  
mongo_port = 27017
mongo_db_name = "ecommerce" 

#informações do Postegres

postgres_host = "postgres"  
postgres_port = 5432
postgres_db_name = "pb_dw"
postgres_user = "root"
postgres_password = "root"

#conenão com mongo
mongo_client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
mongo_db = mongo_client[mongo_db_name]

#conenão com postgress
postgres_conn = psycopg2.connect(
    dbname=postgres_db_name,
    user=postgres_user,
    password=postgres_password,
    host=postgres_host,
    port=postgres_port
)

#extrair dados do mongo
def extract_data_from_mongo():
    collection = mongo_db['order_reviews']  
    documents = collection.find()
    return list(documents)

#extrair dados dos arquivos csv
def read_csv_to_dict_list(file_path):
    data = []
    try:
        with open(file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Arquivo CSV não encontrado em {file_path}")
    return data

#finção para executar querys no postegress
def execute_postegres_query(query):

    try:
        # Criando um cursor
        cursor = postgres_conn.cursor()

        # Executando o comando SQL para criar a tabela
        cursor.execute(query)

        # Commit das alterações no banco de dados
        postgres_conn.commit()

        # Fechando a conexão e o cursor
        cursor.close()

        print("Query executada!")

    except psycopg2.Error as e:
        print(f"Erro ao executar query: {e}")

# Função para inserir dados na tabela Dimensão do Pedido
def insert_data_into_order_dimension(data):
    try:
        cursor = postgres_conn.cursor()
        insert_query = """
        INSERT INTO dimensao_pedido (order_id, customer_id, order_status, order_purchase_timestamp, 
        order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        for row in data:
            for date_column in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
                if row[date_column] == '':
                    row[date_column] = None  # Define campos de data vazios como NULL

            cursor.execute(insert_query, (
                row['order_id'],
                row['customer_id'],
                row['order_status'],
                row['order_purchase_timestamp'],
                row['order_approved_at'],
                row['order_delivered_carrier_date'],
                row['order_delivered_customer_date'],
                row['order_estimated_delivery_date']
            ))

        postgres_conn.commit()
        cursor.close()
        print("Dados inseridos na tabela Dimensão do Pedido.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela Dimensão do Pedido: {e}")

# Função para inserir dados na tabela Dimensão do Cliente
def insert_data_into_customer_dimension(data):
    try:
        cursor = postgres_conn.cursor()
        insert_query = """
        INSERT INTO dimensao_cliente (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
        VALUES (%s, %s, %s, %s, %s);
        """
        for row in data:
            cursor.execute(insert_query, (
                row['customer_id'],
                row['customer_unique_id'],
                row['customer_zip_code_prefix'],
                row['customer_city'],
                row['customer_state']
            ))
        postgres_conn.commit()
        cursor.close()
        print("Dados inseridos na tabela Dimensão do Cliente.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela Dimensão do Cliente: {e}")

# Função para inserir dados na tabela Dimensão de Produto
def insert_data_into_product_dimension(data):
    try:
        cursor = postgres_conn.cursor()
        insert_query = """
        INSERT INTO dimensao_produto (product_id, product_category_name, product_name_length, 
            product_description_length, product_photos_qty, product_weight_g, product_length_cm,
            product_height_cm, product_width_cm)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        for row in data:
            # Tratar campos vazios como NULL
            for numeric_column in ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']:
                if row[numeric_column] == '':
                    row[numeric_column] = None

            cursor.execute(insert_query, (
                row['product_id'],
                row['product_category_name'],
                row['product_name_lenght'],
                row['product_description_lenght'],
                row['product_photos_qty'],
                row['product_weight_g'],
                row['product_length_cm'],
                row['product_height_cm'],
                row['product_width_cm']
            ))
        postgres_conn.commit()
        cursor.close()
        print("Dados inseridos na tabela Dimensão de Produto.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela Dimensão de Produto: {e}")

# Função para inserir dados na tabela Dimensão de Pagamento
def insert_data_into_payment_dimension(data):
    try:
        cursor = postgres_conn.cursor()
        insert_query = """
        INSERT INTO dimensao_pagamento (order_id, payment_sequential, payment_type, payment_installments, payment_value)
        VALUES (%s, %s, %s, %s, %s);
        """
        for row in data:
            cursor.execute(insert_query, (
                row['order_id'],
                row['payment_sequential'],
                row['payment_type'],
                row['payment_installments'],
                row['payment_value']
            ))
        postgres_conn.commit()
        cursor.close()
        print("Dados inseridos na tabela Dimensão de Pagamento.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela Dimensão de Pagamento: {e}")

# Função para preencher a coluna `order_review` com os dados coletados do MongoDB
def update_order_review_data(reviews):
    try:
        cursor = postgres_conn.cursor()
        update_query = """
        UPDATE dimensao_pedido
        SET order_review = %s
        WHERE order_id = %s;
        """
        for review in reviews:
            review_data = review["review_score"]
            cursor.execute(update_query, (review_data, review["order_id"]))
        postgres_conn.commit()
        cursor.close()
        print("Dados da coluna 'order_review' atualizados na tabela Dimensão do Pedido com 'review_score'.")
    except psycopg2.Error as e:
        print(f"Erro ao atualizar os dados da coluna 'order_review' com 'review_score': {e}")

# Função para inserir dados na tabela Dimensão de Order Item
def insert_data_into_order_item_dimension(data):
    try:
        cursor = postgres_conn.cursor()
        insert_query = """
        INSERT INTO dimensao_order_item (order_id, product_id, seller_id, shipping_limit_date, price, freight_value)
        VALUES (%(order_id)s, %(product_id)s, %(seller_id)s, %(shipping_limit_date)s, %(price)s, %(freight_value)s);
        """
        cursor.executemany(insert_query, data)
        postgres_conn.commit()
        cursor.close()
        print(f"{len(data)} registros inseridos na tabela Dimensão Order Item.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela Dimensão Order Item: {e}")

#dados do csv
customers = read_csv_to_dict_list('/python_etl/input/olist_customers_dataset.csv') #Endereço do cliente
order_item = read_csv_to_dict_list('/python_etl/input/olist_order_items_dataset.csv') #Dados da compra de um item
order_payments = read_csv_to_dict_list('/python_etl/input/olist_order_payments_dataset.csv') #Dados de pagamentos
orders = read_csv_to_dict_list('/python_etl/input/olist_orders_dataset.csv') #Dados status da compra
products = read_csv_to_dict_list('/python_etl/input/olist_products_dataset.csv') #Dados status da compra

#dados do mongo
mongo_data = extract_data_from_mongo() #Review de compra

# Define a query para criar a tabela Dimensão do Pedido
create_order_dimension_table_query = """
CREATE TABLE IF NOT EXISTS dimensao_pedido (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    order_status VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);
"""

# Criara tabela Dimensão do Pedido
execute_postegres_query(create_order_dimension_table_query)

# Insere os dados das tabelas de origem na tabela Dimensão do Pedido
insert_data_into_order_dimension(orders)

# Define a query para criar a tabela Dimensão do Cliente
create_customer_dimension_table_query = """
CREATE TABLE IF NOT EXISTS dimensao_cliente (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR
);
"""

# Criara tabela Dimensão do Pedido
execute_postegres_query(create_customer_dimension_table_query)

# Inserir dados na tabela Dimensão do Cliente
insert_data_into_customer_dimension(customers)

# Define a query para criar a tabela Dimensão do Produto
create_product_dimension_table_query = """
CREATE TABLE IF NOT EXISTS dimensao_produto (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g INTEGER,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);
"""

# Criara tabela Dimensão do Produto
execute_postegres_query(create_product_dimension_table_query)

# Inserir dados na tabela Dimensão do Produto
insert_data_into_product_dimension(products)

# Define a query para criar a tabela Dimensão do Pagamento
create_payment_dimension_table_query = """
CREATE TABLE IF NOT EXISTS dimensao_pagamento (
    order_id VARCHAR,
    payment_sequential INTEGER,
    payment_type VARCHAR,
    payment_installments INTEGER,
    payment_value NUMERIC
);
"""

# Criara tabela Dimensão do Pagamento
execute_postegres_query(create_payment_dimension_table_query)

# Inserir dados na tabela Dimensão do Pagamento
insert_data_into_payment_dimension(order_payments)

# Define a query para criar a coluna order_review na dimensao pedido 
create_order_review_column_in_order_table_query = """
    ALTER TABLE dimensao_pedido
    ADD COLUMN order_review INTEGER;
"""

# Adicionar a coluna `order_review` à tabela de dimensão "pedido"
execute_postegres_query(create_order_review_column_in_order_table_query)

# Preencher a coluna `order_review` com a coluna `review_score` do MongoDB
update_order_review_data(mongo_data)


#Define a query para criar tabela dimensao order item
create_table_dimesion_order_item_query = """
CREATE TABLE IF NOT EXISTS dimensao_order_item (
    order_item_id SERIAL PRIMARY KEY,
    order_id VARCHAR,
    product_id VARCHAR,
    seller_id VARCHAR,
    shipping_limit_date TIMESTAMP,
    price NUMERIC,
    freight_value NUMERIC
);
"""

#Cria tabela dimensao order item 
execute_postegres_query(create_table_dimesion_order_item_query)

#Insere dados em dimensao_order_item
insert_data_into_order_item_dimension(order_item)

# Define a query para criar tabela fato de vendas
create_fact_order_table_query = """
CREATE TABLE IF NOT EXISTS fato_vendas (
    sale_id SERIAL PRIMARY KEY,
    order_id VARCHAR,
    product_id VARCHAR,
    customer_id VARCHAR,
    payment_type VARCHAR,
    order_date TIMESTAMP,
    review_score INTEGER
);
"""

# Criara tabela Fato de Vendas
execute_postegres_query(create_fact_order_table_query)

insert_query = """
    INSERT INTO fato_vendas (order_id, product_id, customer_id, payment_type, order_date, review_score)
    SELECT
        dp.order_id,
        doi.product_id,
        dc.customer_id,
        dpay.payment_type,
        dp.order_purchase_timestamp,
        dp.order_review
    FROM dimensao_pedido dp
    JOIN dimensao_cliente dc ON dp.customer_id = dc.customer_id
    JOIN dimensao_pagamento dpay ON dp.order_id = dpay.order_id
    JOIN dimensao_order_item doi ON dp.order_id = doi.order_id;    
"""

execute_postegres_query(insert_query)

select_query = """
SELECT * FROM fato_vendas;
"""

try:
    cursor = postgres_conn.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()

    # Imprimir os dados
    for row in result:
        print(row)
except psycopg2.Error as e:
    print(f"Erro ao selecionar dados: {e}")

postgres_conn.close()
