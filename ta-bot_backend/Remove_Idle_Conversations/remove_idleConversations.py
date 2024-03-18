import redis
from redis.commands.json.path import Path
import pymongo
import json
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from TaBotRadis import RedisCache
from mongodb import MongoDB
from conversation import Conversation


load_dotenv()


#MongoDB
mongo_username=os.environ.get("MONDO_DB_USER")
mongo_password=os.environ.get("MONGO_DB_PASSWORD")
mongo_host=os.environ.get("MONGO_DB_HOST")
mongo_port=os.environ.get("MONGO_DB_PORT")

#Redis
redis_username=os.environ.get("REDIS_USER")
redis_password=os.environ.get("REDIS_PASSWORD")
redis_host=os.environ.get("REDIS_HOST")
redis_port=os.environ.get("REDIS_PORT")

redis_client = RedisCache(
    username=redis_username,
    password=redis_password,
    host=redis_host,
    port=redis_port
    ).create_connection()


Mongo=MongoDB(
    username=mongo_username,
    password=mongo_password,
    host=mongo_host,
    port=mongo_port
    )


mongo_client=Mongo.connect_mongodb()
db=mongo_client['ta_bot']
mongo_collection=db['conversations']



def remove_idle_conversations():
    current_time = datetime.now()

    # Get all conversation keys from Redis
    conversation_keys = redis_client.keys('*')

    for key in conversation_keys:
        conversation_id = key.decode()
        conversation_data = redis_client.json().get(conversation_id)
        
        if conversation_data and 'last_event' in conversation_data:
            last_event_time_str = conversation_data['last_event'][0]
            print(last_event_time_str)

            try:
                last_event_time = datetime.strptime(last_event_time_str, r'%Y-%m-%d %H:%M:%S.%f')
            except ValueError as e:
                print(f"Error parsing last_event_time: {e}")
                print(f"Conversation ID: {conversation_id}")
                print(f"last_event_time_str: {last_event_time_str}{type(last_event_time_str)}")
                print("")
                continue

            idle_duration = current_time - last_event_time

            print(f"Conversation ID: {conversation_id}")
            print(f"Last Event Time: {last_event_time}")
            print(f"Idle Duration: {idle_duration}")
            print("")

            if idle_duration >= timedelta(minutes=5):
                # Move the idle conversation to MongoDB
                Conversation.end_conversation_Mongo(
                    mongo_client=mongo_client,
                    conversation_ID=conversation_id,
                    last_event=str(current_time),
                    end_time=str(current_time),
                    messages=conversation_data['messages']
                )
                # Remove the conversation from Redis
                redis_client.delete(conversation_id)
                print('Deleted Conversation' + str(conversation_id) + ': Start:- ' + str(conversation_data['start']) + ': End:-' + str(conversation_data['end']))


if __name__ == "__main__":
    while True:
        print('Deleting Idle Conversations, Idle for more than 5 mins')
        remove_idle_conversations()
        # Sleep for a specified interval (e.g., 1 minute)
        time.sleep(60)
