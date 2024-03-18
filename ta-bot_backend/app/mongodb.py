from pymongo.mongo_client import MongoClient
from pymongo import errors
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime

class MongoDB:
    def __init__(self, username, password,host,port):
        self.username = username
        self.password = password
        self.host=host
        self.port=port
        

    def connect_mongodb(self):
        try:
            # Construct the URI with username and password
            uri_with_auth = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/ta_bot?authMechanism=DEFAULT"
            client = MongoClient(uri_with_auth, server_api=ServerApi('1'))
            return client
        except errors.ConnectionFailure as e:
            print(f"Connection to MongoDB failed: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def initiate_mongo(self):
        mongo_client = self.connect_mongodb()
        db_name = "ta_bot"
        try:
            # Check if the database already exists
            if db_name not in mongo_client.list_database_names():
                # Create the database by inserting a sample document
                db = mongo_client[db_name]
                collection = db["conversations"]
                sample_doc = {"db_created": datetime.now()}
                collection.insert_one(sample_doc)
        except errors.ConnectionFailure as e:
            print(f"Connection to MongoDB failed: {e}")
            return
        except errors.ServerSelectionTimeoutError as e:
            print(f"Server selection timeout: {e}")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        finally:
            # Close the MongoDB client connection
            mongo_client.close()
            return
