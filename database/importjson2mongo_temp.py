import pymongo
from pymongo import MongoClient
import json


class Json2Mongo(object):
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 27107
        #create mongo client
        self.client = MongoClient(self.host, self.port)
        #create database dialog
        self.db = self.client.dialog
        # create collection scene
        self.collection = self.db.scene

    #write json to db
    def write_database(self):
        with open('cedict.json', 'r') as f:
            json_data = json.load(f)
        data = {
            "name": "CC-CEDICT",
            "content": json_data
        }
        try:
            myquery = {"name": "CC-CEDICT"}
            self.collection.update(myquery, data, upsert = True)
            print("import json to mongoDB successfully.")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # jm = Json2Mongo()
    # jm.write_database()

    # create a database named c2eDB and a collention named c2ecol under it
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    c2eDB = myclient["c2eDB"]
    c2ecol = c2eDB["c2ecol"]
    # mydb = myclient["runoobdb"]
    # mycol = mydb["sites"]
    # mylist =[
    #     {"word": "你好", "trans": "hello; how do you do"},
    #     {"word": "早上", "trans": "morning"}
    #           ]
    # x = mycol.insert_many(mylist)
    # myquery = {"word": "早上"}
    # mydoc = mycol.find(myquery)
    # for x in mydoc:
    #     print(x)
