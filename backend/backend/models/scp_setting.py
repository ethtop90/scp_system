from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class scp_setting:
    def __init__(self, type, mg_title, pt_name, source):
        self.type = type
        self.mg_title = mg_title
        self.pt_name = pt_name
        self.source = source
        self.pt_start_time = None
        self.up_settings = None