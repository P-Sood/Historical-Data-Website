import pymongo
from pymongo import MongoClient
# connection to cluster

class DataBase():
    def __init__(self,username,password,database_name,collection_name):
        self.username = username
        self.password = password
        self.database_name = database_name
        self.collection_name = collection_name

    def connection(self):
        try:
            self.cluster = MongoClient("mongodb+srv://" + self.username + ":" + self.password + "@cluster0.luyxz.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")
            self.database = self.cluster[self.database_name]
            self.collection = self.database[self.collection_name]
        except:
            print("Your username or password was incorrect, please try again \n")
    
    def insert_one(self,dictionary):
        self.collection.insert_one(dictionary)
    

    # Query is a dictionary
    def find(self,query,field = None): 
        results = self.collection.find(query)
        try:
            for result in results:
                print(result[field])
        except:
            for result in results:
                print(result) 

    def count(self,query):
        numDocuments = self.collection.count_documents(query)
        print(numDocuments)

    
