from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class Scp_setting:
    def __init__(self,id ,username, type, mg_title, pt_name, source):
        self.id = id
        self.username = username
        self.type = type # site|file
        self.mg_title = mg_title
        self.pt_name = pt_name
        self.source = source
        self.pt_start_time = None
        self.up_settings = None