import os
import sys
sys.path.append(os.path.abspath('./'))

import pymongo
from config import MONGO_URL

client = pymongo.MongoClient(MONGO_URL)
db = client.ntu_badoo.profiles

def send_mongodb(data):
    db.insert_one(data)

def get_form(user_id):
    return db.find_one({'user_id': f'{user_id}'})

def update_form(user_id, data):
    current = {'user_id': f'{user_id}'}
    db.update_one(current, {'$set': data})

def form_exists(user_id):
    if get_form(user_id) is None: return False
    else: return True

def get_all_forms(user_id):
    data = [data for data in db.find({}) if data['user_id'] != user_id]
    return data

def get_forms_by_tags(user_id):
    user_tags = db.find_one({'user_id': f'{user_id}'})['tags']
    if user_tags is None:
        return []

    all_users = get_all_forms(user_id)
    result_users = []

    for user in all_users:
        tag_count = 0

        for tag in user_tags:
            if tag in user['tags']:
                tag_count += 1
        
        if tag_count >= 1:
            result_users.append(user)

    return result_users