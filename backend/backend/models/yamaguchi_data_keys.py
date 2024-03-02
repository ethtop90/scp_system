from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class yamaguchi_data_keys:
    def __init__(self, keys):
        self.keys = keys