from flask import Flask, request, jsonify,session
from flask_session import Session
import openai
import os
from flask_cors import CORS
import openai
import secrets
from dotenv import load_dotenv
import redis
from redis.commands.json.path import Path
from datetime import datetime
import json
from mongodb import MongoDB
from conversation import Conversation
from TaBotRadis import RedisCache 

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET")
CORS(app,origins="*")


load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

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


Mongo.initiate_mongo()
mongo_client=Mongo.connect_mongodb()


def handle_request():
    # Handle preflight request
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://0.0.0.0')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        return response

@app.route('/', methods=['OPTIONS'])
def handle_request():
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', 'http://0.0.0.0')  # Update with your frontend URL
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response



@app.route('/', methods=['GET'])
def home():
     return "<h1 style='color:blue'>Hello There!</h1>"

# #---------------------------Session Initiation----------------------------------------
@app.route('/initiate_session')
def initiate_session():

    conversation_ID = secrets.token_hex(4)
    conversation_data=Conversation.initiate_session(conversation_ID)
   
    # Store the conversation data in Redis
    redis_client.json().set(conversation_ID,Path.root_path(),conversation_data )
    #Store the conversation in mongo
    Conversation.create_conversation(mongo_client=mongo_client,document=conversation_data)

    return jsonify({'convID': conversation_ID})

# #-------------------------------------------------------------------------------------------
@app.route('/api/TA_BOT', methods=['GET', 'OPTIONS'])
def generate_response():
    if request.method == 'OPTIONS':
        return handle_request()

    elif request.method == 'GET':
        question = str(request.args.get('question'))
        conversationID=str(request.args.get('conversationID'))
        conversation_data = redis_client.json().get(conversationID)

        
        conversation_data['messages'].append(
            {
                "role": "user",
                "content": question
            }
        )

        print(conversation_data['messages'])

        # #Make API Call to fine tuned model
        response =  openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:ta-bot-ai-application-for-education-project-university-of-colombo-school-of-computing::859DT7v1",
            messages=conversation_data['messages'],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response=str(response["choices"][0]["message"]["content"])  
    
        print(response)

        conversation_data['messages'].append(
            {
                "role": "assistant",
                "content": response
            }
        )
        conversation_data['last_event']=str(datetime.now()),

        redis_client.json().set(conversationID,Path.root_path(),conversation_data)
        Conversation.update_conversation_Mongo(
             mongo_client=mongo_client,
             conversation_ID=conversationID,
             last_event=conversation_data["last_event"],
             messages=conversation_data["messages"]
        )

     
        return jsonify({'results': response})  # Return the data as JSON

    else:
        return jsonify({'results': 'Invalid request method'})  # Return an error response as JSON


# # ------------END CONVERSATION------------------------
@app.route('/end_conversation', methods=['POST'])
def store_conversation():
    conversationID=str(request.args.get('conversationID'))
    conversation_data = redis_client.json().get(conversationID)
    print(conversation_data)

    # # Store conversation data in MongoDB
    Conversation.end_conversation_Mongo(
                    mongo_client=mongo_client,
                    conversation_ID=conversationID,
                    last_event=str(datetime.now()),
                    end_time=str(datetime.now()),
                    messages=conversation_data['messages']
                    )
                # Remove the conversation from Redis
    redis_client.delete(conversationID)

    print("Conversation Sucessfully deleated:   "+conversationID)

    return jsonify({'message': 'Conversation stored in MongoDB and deleted from Redis'})




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
