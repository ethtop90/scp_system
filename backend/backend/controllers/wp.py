from app import app, mongo, bcrypt
from flask import Flask, Blueprint, jsonify, request
from flask_cors import cross_origin
from utils.wp_user.wp_user import *
from models.wp_user import *

# Create a Blueprint named 'wp'
wp = Blueprint('wp', __name__, url_prefix='/wp')

# Define a route for '/users' on the 'wp' Blueprint
@wp.route('/users', methods=['GET'])
def wp_users():
    # Dummy function to return a response for demonstration
    username = request.args.get('username')
    users, user_id, application_password = get_user_list(username)
    # update wp_users collection
    try:
        for user in users:
            wp_user = Wp_user(user['id'], user['name'])
            mongo.db.wp_users.insert_one({"id": user['id'], "username": user['name']})
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500
    return jsonify({"users": users, "user_id": user_id, "application_password": application_password})

# Define a route for '/login' on the 'wp' Blueprint
@wp.route('/login', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def wp_login():
    # Dummy function to return a response for demonstration
    # Normally, you'd handle authentication logic here
    
    return jsonify({"message": "Login endpoint reached"})

# Define a route for '/posts' on the 'wp' Blueprint
@wp.route('/posts', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def wp_posts():
    # Dummy function to return a response for demonstration
    return jsonify({"message": "Posts endpoint reached"})

app.register_blueprint(wp)

