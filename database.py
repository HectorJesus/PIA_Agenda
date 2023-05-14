from pymongo.mongo_client import MongoClient
import certifi

MONGO_URI = "mongodb+srv://Hector:Hector@cluster0.ru5ciy5.mongodb.net/?retryWrites=true&w=majority"
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_agenda_app"]
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except ConnectionError:
        print("Error de conexion con la DB")
    return db

