from app import mongo, bcrypt

db = mongo.db

class yamaguchi_data_keys:
    def __init__(self, keys):
        self.keys = keys