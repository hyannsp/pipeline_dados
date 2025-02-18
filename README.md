# Pipeline de Dados - MongoDB e MySQL

## 📌 Sobre o Projeto

Este projeto foi criado como um método de prática para consolidação do que aprendi no curso ***Pipeline de dados: integrando Python com MongoDB e MySQL*** da plataforma **Alura**, unificando o aprendido com uma estruturação orientada à objetos, implementando um pipeline de dados que integra bancos de dados MongoDB e MySQL, permitindo a extração, transformação e carga (ETL) de dados.

## 🎲 Banco de Dados

- MongoDB

    - Conexão com MongoDB Atlas

    - Inserção, busca, atualização e remoção de documentos

    - Conversão de coleções para DataFrames Pandas

    - Manipulação de atributos nas coleções

- MySQL

    - Conexão com banco MySQL

    - Criação e uso de bancos de dados

    - Criação de tabelas de forma dinâmica

    - Inserção de registros utilizando listas de valores

## 🔧 Tecnologias Utilizadas

- Python 3.x

- Pandas (manipulação de dados)

- MySQL Connector (conexão MySQL)

- PyMongo (integração com MongoDB)

- Requests (consumo de APIs externas)

## 🔄 Fluxo do Pipeline
1. **Extração**: Coleta de dados de uma API pública
2. **Transformação**: Armazenamento inicial no MongoDB e formatação dos dados
3. **Criação** de CSVs: Extração de dados relevantes para arquivos CSV
4. **Carga no MySQL**: Criação de tabelas e inserção dos dados dos CSVs

## ⚙️ Como Configurar e Executar

**1️. Configurar Ambiente Virtual**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

**2. Instalar Dependências**
```bash
pip install -r dependencies/requirements.txt
```

**3️. Configurar Credenciais**

Crie um arquivo .env dentro da pasta config/ e adicione as credenciais necessárias:
```bash
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=senha
```
**4️. Executar o Pipeline!**