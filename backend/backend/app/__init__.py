from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from waitress import serve


# test api
from routes import bp
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import secrets



# real api

app = Flask(__name__, static_folder='../../../frontend/build', static_url_path='/')
# app = Flask(__name__)

app.config['MAIN_URL'] = 'http://localhost:3000/'
# app.config['MAIN_URL'] = 'http://pationonline.ir/'
# CORS(app, resources={r"/*": {"origins": }})
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True

app.config['MONGO_URI'] = 'mongodb://root:H4QpE7IY4Zqa5CjIksqzqSfS@localhost:27017/scrapping_sys'  # Replace with your MongoDB URI

strong_secret_key = secrets.token_urlsafe(32)

# Assign the secret key to app.config['JWT_SECRET_KEY']
app.config['JWT_SECRET_KEY'] = strong_secret_key

jwt = JWTManager(app)
mongo = PyMongo(app, uri='mongodb://localhost:27017/scp_system')
bcrypt = Bcrypt(app)

@app.errorhandler(404)
def not_found(e):
  return app.send_static_file('index.html')

import controllers


# serve(app, host='0.0.0.0', port=5000, threads=1) #WAITRESS!
