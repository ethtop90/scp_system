from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class Scp_url:
    def __init__(self,name, url, type):
        self.name = name
        self.url = url
        self.type = type