from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

class User:
    def __init__(self, db):
        self.collection = db.users
    
    def create_user(self, user_data):
        user_data['created_at'] = datetime.datetime.utcnow()
        user_data['updated_at'] = datetime.datetime.utcnow()
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        return self.collection.find_one({'email': email})
    
    def update_user(self, user_id, update_data):
        update_data['updated_at'] = datetime.datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(user_id)}, 
            {'$set': update_data}
        )
