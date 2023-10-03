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



#dados do csv
customers = read_csv_to_dict_list('/python_etl/input/olist_customers_dataset.csv') #Endereço do cliente
order_item = read_csv_to_dict_list('/python_etl/input/olist_order_items_dataset.csv') #Dados da compra de um item
order_payments = read_csv_to_dict_list('/python_etl/input/olist_order_payments_dataset.csv') #Dados de pagamentos
orders = read_csv_to_dict_list('/python_etl/input/olist_orders_dataset.csv') #Dados status da compra
products = read_csv_to_dict_list('/python_etl/input/olist_products_dataset.csv') #Dados status da compra

#dados do mongo
mongo_data = extract_data_from_mongo() #Review de compra

query = """

"""
execute_postegres_query(query)

postgres_conn.close()
