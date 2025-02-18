from utils import handle_exceptions
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class _Mongo:
    def __init__(self, uri, db_name, collection_name):
        self.client = self.__connect_mongo(uri)
        self.db = self.__create_connect_db(db_name)
        self.collection = self.__create_connect_collection(collection_name)

    def __connect_mongo(self, uri):
        try:
            client = MongoClient(uri, server_api=ServerApi('1'))
            client.admin.command('ping')
            print("Pinged your deployment. Successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def __create_connect_db(self, db_name):
        if not db_name:
            raise ValueError("Database name cannot be None or empty")
        return self.client[db_name]

    def __create_connect_collection(self, collection_name):
        if not collection_name:
            raise ValueError("Collection name cannot be None or empty")
        return self.db[collection_name]
    
    @handle_exceptions
    def insert_one(self, document):
        result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
        return result.inserted_id

    @handle_exceptions
    def insert_many(self, documents):
        result = self.collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents")
        return result.inserted_ids
    
    @handle_exceptions
    def find_one(self, query):
        document = self.collection.find_one(query)
        if document:
            print(f"Found document: {document}")
        else:
            print("No document found")
        return document

    @handle_exceptions
    def find_many(self, query={}):
        documents = list(self.collection.find(query))
        print(f"Found {len(documents)} documents")
        return documents
    
    @handle_exceptions
    def delete_one(self, query):
        result = self.collection.delete_one(query)
        print(f"Deleted {result.deleted_count} document")
        return result.deleted_count

    @handle_exceptions
    def delete_many(self, query):
        result = self.collection.delete_many(query)
        print(f"Deleted {result.deleted_count} documents")
        return result.deleted_count

    @handle_exceptions
    def update_one(self, query, update):
        result = self.collection.update_one(query, update)
        print(f"Updated {result.modified_count} document")
        return result.modified_count

    @handle_exceptions
    def update_many(self, query, update):
        result = self.collection.update_many(query, update)
        print(f"Updated {result.modified_count} documents")
        return result.modified_count

    @handle_exceptions
    def close_connection(self):
        self.client.close()
        print("MongoDB connection closed.")
