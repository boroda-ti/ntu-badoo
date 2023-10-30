import os
import sys
sys.path.append(os.path.abspath('./'))

import pymongo
from config import MONGO_URL

client = pymongo.MongoClient(MONGO_URL)
db = client.ntu_badoo.profiles

def send_mongodb(data):
    db.insert_one(data)