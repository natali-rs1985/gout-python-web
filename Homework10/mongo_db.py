import pymongo
from pymongo.database import Database
from pymongo.collection import Collection


cont_uri = "mongodb://admin:123qwe@localhost:27017/assistant?retryWrites=true&w=majority"

client = pymongo.MongoClient(cont_uri)
assistant: Database = client.assistant
contacts_collection: Collection = assistant.contacts


