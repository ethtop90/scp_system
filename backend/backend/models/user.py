from app import mongo, bcrypt

db = mongo.db

class User:
    def __init__(self, username, email, password):
      self.username = username
      self.email = email
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
