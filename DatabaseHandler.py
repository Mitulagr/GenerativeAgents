# This file contains the class DBHandler which is responsible for handling the database

from pymongo import MongoClient
from Memories import *
from Params import agentsDetails
from dotenv import load_dotenv
import os

load_dotenv('Config/.env')

# MongoDB connection [MongoDB接続]
client = MongoClient(os.getenv('MongoDB_ID'))

class DBHandler:
    def __init__(self):
        self.memoriesDB = client["memories_DB"]
        self.agentCollection = {}
        self.initDB()

    def initDB(self):
        collection_names = self.memoriesDB.list_collection_names()
        for collection in collection_names:
            self.memoriesDB[collection].drop()
        for agent in agentsDetails:
            self.agentCollection[agent["name"]]=self.memoriesDB[agent["name"]]

    # Adding and getting memories from the database [データベースへのメモリーの追加と取得]
    def addMemories(self, name, memory):
        d = {'observation':memory.observation,
            'creation':memory.creation,
            'lastAccess':memory.lastAccess,
            'importance':memory.importance}
        self.agentCollection[name].insert_one(d)
    
    # Getting all memories from the database [データベースからすべてのメモリを取得する]
    def getAllMemories(self, name):
        d = self.agentCollection[name].find()
        memories_list = []
        for item in d:
            memory = Memory()
            memory._id = item['_id']
            memory.observation = item['observation']
            memory.creation = item['creation']
            memory.lastAccess = item['lastAccess']
            memory.importance = item['importance']
            memories_list.append(memory)
        return memories_list
    
    # Getting a specific memory from the database [データベースから特定のメモリを取得する]
    def updateMemories(self,name,memory_id,field,value):
        query = {'_id': memory_id}
        update = {'$set': {field: value}}
        self.agentCollection[name].update_one(query, update)
DB = DBHandler()