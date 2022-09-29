import pymongo
from urllib.parse import quote_plus

username = quote_plus('thanhthai')
password = quote_plus('taokobietaA165')

client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@cluster0.i1qojrx.mongodb.net/?retryWrites=true&w=majority".format(username, password))
db = client.flask_tutorial

table_animal = db['animal']
