from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class User:
    def __init__(self, username, email, password):
      self.username = username
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
