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
postgres_db_name = "postgre"
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
#execute_postegres_query(create_order_dimension_table_query)

# Insere os dados das tabelas de origem na tabela Dimensão do Pedido
#insert_data_into_order_dimension(orders)

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
#execute_postegres_query(create_customer_dimension_table_query)

# Inserir dados na tabela Dimensão do Cliente
#insert_data_into_customer_dimension(customers)

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
#execute_postegres_query(create_product_dimension_table_query)

# Inserir dados na tabela Dimensão do Produto
#insert_data_into_product_dimension(products)

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

select_query = """
SELECT * FROM dimensao_pagamento;
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
