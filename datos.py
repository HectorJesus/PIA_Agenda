from pymongo import MongoClient
from bson import json_util
from flask import Flask, render_template
from database import dbConnection

database = dbConnection()

collection = database['users']

documents = collection.find({})

data = []
for doc in documents:
    json_data = json_util.dumps(doc)
    data.append(json_data)
