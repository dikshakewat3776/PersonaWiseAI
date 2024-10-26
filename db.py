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


def get_conversations(user_id):
    last_conversation = list(db[CONVERSATIONS_COLLECTION].find({'user_id': user_id}).sort('_id', -1).limit(1))
    # Return the last conversation or an empty list if none exists
    print("fetched the conversation: ", str(last_conversation))
    return last_conversation if last_conversation else []
    #     return [{
    #   "_id": {
    #     "$oid": "671c20f5269b481ca33aa98b"
    #   },
    #   "user_id": {
    #     "$numberLong": "1729896674718"
    #   },
    #   "user_input": "How old are you?",
    #   "bot_response": {
    #     "Hello! I’m PersonaWiseAI, your personal financial assistant. To help you build a tailored financial profile, please share your financial and demographic information.": "ok",
    #     "What’s your monthly income?": "30000",
    #     "What are your monthly expenses?": "2000",
    #     "Do you have any assets? (e.g., property, savings)": "1 property",
    #     "What are your liabilities? (e.g., loans, debts)": "3 loans",
    #     "How old are you?": "29"
    #   },
    #   "timestamp": {
    #     "$date": "2024-10-26T04:21:33.385Z"
    #   }
    # }]
