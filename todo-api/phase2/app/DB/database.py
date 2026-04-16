from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client = None 
    db = None
    
    @classmethod
    def initialize(cls):
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("DB_NAME", "todo_app")
        
        try:
            cls.client = MongoClient(uri)
            cls.db = cls.client[db_name]
            cls.client.admin.command('ping')
            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e
        
    @classmethod
    def get_collection(cls, collection_name):
        if cls.db is None:
            cls.initialize()
        return cls.db[collection_name]