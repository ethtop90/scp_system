from app import app
from utils.wp_user.wordpress_login import wordpress_login
from flask import request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
   

@app.route('/wp-login', methods = ['POST'])
def wp_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    application_password = data.get('applicationPassword')

    cookies = wordpress_login(username, password)
    session['username'] = username
    print(username)
    access_token = create_access_token(identity=username)
    if cookies:
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'cookies': cookies, 'username': username, 'application_password': application_password}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
