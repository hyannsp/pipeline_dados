import os
from mongo_dataframe import MongoDataFrame
from bd_produtos import BdProdutos
import requests

if __name__ == "__main__":

    ### Extração e Salvamento de Dados ###
    # Criação do database e collection
    """
    A URI foi salva dentro do ambiente virtual VENV, inserindo-a adicionando o código abaixo ao final do arquivo venv/bin/activate
    export MONGO_URI="mongodb+srv://usuario:senha@cluster.mongodb.net"
    Assim fica protegida para mim, no meu usuário!
    """
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI not defined in virtual enviroment!")
    
    mongo = MongoDataFrame(uri, "db_produtos", "produtos")

    # Dados CApturando dados da API
    url = os.getenv("API_URL")
    response = requests.get(url)

    # Inserindo dados da API no Mongo
    mongo.insert_many(response.json())

    ### Tratamento dos Dados ###
    # Renomeando as colunas de lat -> latitude e lon -> longitude
    mongo.update_many({}, {"$rename": {"lat": "latitude", "lon": "longitude"}})

    # Carregando como dataframes caso queira um df insira aqui com a query (e nome caso precise)
    mongo.load_to_dataframe({"Categoria do Produto" : "livros"}, "tabela_livros")
    mongo.load_to_dataframe({"Data da Compra": {"$regex": "/202[1-9]$"}}, "tabela_+2021")
    
    # Ajustando as datas para todos os df criados
    for df in mongo.dfs.keys():
        mongo.format_date_columns(df, columns_name=["Data da Compra"], date_format="%d/%m/%Y")
    
    # Exportando os dfs como csv para a pasta /data
    for df in mongo.dfs.keys():
        mongo.save_to_csv(df, f"./data/{df}.csv")

    ### Inserindo os dados no MySQL ###
    # Conectando ao mysql e criando e se conectando à um database
    mysql_db = BdProdutos(host = os.getenv("DB_HOST"), user = os.getenv("DB_USERNAME"), password = os.getenv("DB_PASSWORD"))
    mysql_db.create_database("db_produtos")
    mysql_db.show_databases()
    mysql_db.use_database("db_produtos")

    # Criando uma tabela e a populando
    fields = {
        "id": "VARCHAR(100)",
        "Produto": "VARCHAR(100)",
        "Categoria_Produto": "VARCHAR(100)",
        "Preco": "FLOAT(10,2)",
        "Frete": "FLOAT(10,2)",
        "Data_Compra": "DATE",
        "Vendedor": "VARCHAR(100)",
        "Local_Compra": "VARCHAR(100)",
        "Avaliacao_Compra": "INT",
        "Tipo_Pagamento": "VARCHAR(100)",
        "Qntd_Parcelas": "INT",
        "Latitude": "FLOAT(10,2)",
        "Longitude": "FLOAT(10,2)"
    }
    mysql_db.create_table("tb_livros",fields, "id")

    # Inserindo dados
    value_list = mongo.df_to_list("tabela_livros")
    # mysql_db.insert_values_in_table("tb_livros", value_list)

    # Fechando conexões
    mysql_db.close_db_conection()
    mongo.close_connection()

    