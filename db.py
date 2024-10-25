"""
Database interaction module
"""
from pymongo import MongoClient
from datetime import datetime

"""
Configuration settings (MongoDB URI, etc.)
"""

MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "ol_chatbot"
CONVERSATIONS_COLLECTION = "persona-conversations"

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

def store_conversation(user_id, user_input, bot_response):
    try:
        conversation = {
            "user_id": user_id,
            "user_input": user_input,
            "bot_response": bot_response,
            "timestamp": datetime.now()
        }
        # print("---------------------------:" + str(conversation))
        db[CONVERSATIONS_COLLECTION].insert_one(conversation)
    except Exception as e:
        print(e)

def get_conversations():
    return list(db[CONVERSATIONS_COLLECTION].find())