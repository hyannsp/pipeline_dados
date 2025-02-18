import mysql.connector

class BdProdutos:
    def __init__(self, host, user, password):
        self.cnx = self.__connect_to_db(host, user, password)
        self.cursor = self.cnx.cursor()
        self.database = None

    def __connect_to_db(self, host, user, password):
        try:
            cnx = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
            )
            print("Successfully connected to MySQL database!")
            return cnx
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
        
    def close_db_conection(self):
        if not self.cursor:
            print("Database connection is not activated.")
            return
        
        try:
            self.cnx.close()
            print("Conection closed sucefully!")
        except mysql.connector.Error as e:
            print(f"Close connection error: {e}")

    def show_databases(self):
        if not self.cursor:
            print("Database connection is not activated.")
        try:
            self.cursor.execute("show databases;")
            for db in self.cursor:
                print(db)
            return
        except mysql.connector.Error as e:
            print(f"Command error: {e}")
        return
    
    def create_database(self, db_name):
        if not self.cursor:
            print("Database connection is not activated.")
            return
        
        query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
        try:
            self.cursor.execute(query)
            print(f"Database {db_name} created!")
        except mysql.connector.Error as e:
            print(f"Query error: {e}")
        
    def use_database(self, db_name):
        if not self.cursor:
            print("Database connection is not activated.")
            return
        try:
            self.cursor.execute(f"USE {db_name}")
            self.database = db_name
            print(f"Using database {db_name}")
        except mysql.connector.Error as e:
            print(f"Connection error: {e}")

    def create_table(self, table_name, fields, primary_key=None):
        """
        Cria uma tabela no banco de dados.
        
        Parâmetros:
        - table_name (str): Nome da tabela.
        - fields (dict): Dicionário com o nome do campo como chave e o tipo do dado como valor.
        
        Exemplo de `fields`:
        {
            "id": "VARCHAR(100) PRIMARY KEY",
            "Produto": "VARCHAR(100)",
            "Preco": "FLOAT(10,2)",
            "Data_Compra": "DATE"
        }
        """
        if not self.cursor:
            print("Database connection is not activated!")
            return
        
        if not fields:
            print("Cannot create a table without fields!")
            return

        # Construindo a query dinamicamente
        fields_query = ",\n    ".join([f"{col} {dtype}" for col, dtype in fields.items()])
        if primary_key and primary_key in fields:
            fields_query += f",\n    PRIMARY KEY ({primary_key})"

        query = f"CREATE TABLE IF NOT EXISTS {self.database}.{table_name} (\n    {fields_query}\n);"
        print(f"Creating table\n--------------------------------------------\n{query}\n--------------------------------------------")
        try:
            self.cursor.execute(query)
            print(f"Table '{table_name}' creation successful!")
        except mysql.connector.Error as e:
            print(f"Table creation error: {e}")\
            
    def insert_values_in_table(self, tb_name, values_list):
        # values_list = [(1, 2, 33, 1), (2, 1, 44, 3)]
        if not self.cursor or not self.database:
            print("No active database selected!")
            return

        if not values_list:
            print("No values provided for insertion!")
            return
        try:
            # Criar placeholders dinamicamente com base no número de colunas
            columns_size = len(values_list[0])
            placeholders = ", ".join(["%s"] * columns_size)

            # Query dinâmica para inserção
            query = f"INSERT INTO {self.database}.{tb_name} VALUES ({placeholders})"
            print(f"Inserting {len(values_list)} itens in {tb_name}!")
            # Executa a inserção de múltiplas linhas
            self.cursor.executemany(query, values_list)
            self.cnx.commit()

            print(f"Inserted {len(values_list)} rows into '{tb_name}' successfully!")
        except mysql.connector.Error as e:
            print(f"Error inserting into '{tb_name}': {e}") 

    