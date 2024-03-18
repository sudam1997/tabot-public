import os
import secrets
from dotenv import load_dotenv
import redis
from redis.commands.json.path import Path
from datetime import datetime
import json
import secrets

from pymongo.mongo_client import MongoClient
from pymongo import errors
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime


class Conversation():
    def initiate_session(conversation_ID):
        # Create a dictionary for conversation data
        conversation_data = {
            'conversationID': conversation_ID,
            'start':str(datetime.now()),
            'end':'',
            'last_event':str(datetime.now()),
            'messages': [
                    {
                "role": "system",
                "content": "Your are a Teaching Assistant for Software Engineering Course. You should only answer to 'Software Engineering' related questions only. Handle the question not relevant to 'Software Engineering'  gracefully"
            }
            
            ]
        }
        return conversation_data

  
    def create_conversation(mongo_client, document: dict):
        try:
            db = mongo_client['ta_bot']
            collection = db['conversations']
            result = collection.insert_one(document)

            if result.acknowledged:
                print(f"Document inserted with ID: {result.inserted_id}")
            else:
                print("Document insertion failed")
        except ConnectionFailure as e:
            print(f"Connection to MongoDB failed: {e}")
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def end_conversation_Mongo(mongo_client,conversation_ID,end_time,last_event,messages:list):
        try:
            db = mongo_client['ta_bot']
            collection = db['conversations']
            conversation={ "conversationID":conversation_ID}
          
            new_conversation={ 
                "$set":{"end":end_time},
                "$set":{"last_event":last_event}, 
                "$set":{ "messages": messages } 
                }
            
            result = collection.update_one(conversation, new_conversation)

            if result.acknowledged:
                print(f"Conversation Ended Successfully")
            else:
                print("Document insertion failed")
        except ConnectionFailure as e:
            print(f"Connection to MongoDB failed: {e}")
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


            
    def update_conversation_Mongo(mongo_client,conversation_ID,last_event,messages:list):
            try:
                db = mongo_client['ta_bot']
                collection = db['conversations']
                conversation={ "conversationID":conversation_ID}
            
                new_conversation={ "$set":{"last_event":last_event}, "$set":{ "messages": messages } }
                result = collection.update_one(conversation, new_conversation)

                if result.acknowledged:
                    print(f"Document Updated with ID: {result.updated_id}")
                else:
                    print("Document insertion failed")
            except ConnectionFailure as e:
                print(f"Connection to MongoDB failed: {e}")
            except OperationFailure as e:
                print(f"MongoDB operation failed: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
