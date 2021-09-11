from pymongo import MongoClient
from bson.json_util import loads, dumps
import yaml
from os import environ
from pprint import pprint
from dotenv import load_dotenv

from backend.src import helpers as h


if not 'MONGO_INITDB_DATABASE' in environ.keys():
    print("................ mongo environment not loaded, loading ................")
    load_dotenv('mongo/.env', override=True)
    load_dotenv('mongo/.env.dev', override=True)

def connect(
        username=environ['MONGO_INITDB_ROOT_USERNAME'],
        password=environ['MONGO_INITDB_ROOT_PASSWORD']):
    global client, db, projects, users
    client = MongoClient(host=environ['MONGO_HOST'],
                         port=int(environ.get('MONGO_PORT', 27017)),
                         username=username,
                         password=password,
                         authSource=environ['MONGO_INITDB_DATABASE']
                         )
    db = client[environ['MONGO_INITDB_DATABASE']]
    return db

