#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, mongo, bcrypt
from flask import jsonify, request, session, send_from_directory, render_template
from flask_cors import cross_origin
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os

# @cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def serve_react_app(path):
    print(path)
    return app.send_static_file('index.html')
    
@app.route('/login', methods=['GET'])
def login_page():
    return app.send_static_file('index.html')

# @app.route('/<path:path>')
# @cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
# def serve_static(path):
#     return send_from_directory('../../../frontend/build/static', path)

# successful connection
@app.route('/success', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def check_db_connection():
    try:
        mongo.db.command('ping')
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'message': 'Database connection failed', 'error': str(e)}), 500

# Register endpoint
@app.route('/register', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username, email, password)
    print("new_user:", new_user)
    mongo.db.users.insert_one(new_user.__dict__)

    return jsonify({'message': 'User registered successfully'}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = mongo.db.users.find_one({'username': username})
    if user and bcrypt.check_password_hash(user['password'], password):
        session['username'] = user['username']
        session['email'] = user['email']
        print(user['username'])
        access_token = create_access_token(identity=user['email'])
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'username': user['username']}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Logout endpoint
@app.route('/logout', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return jsonify({'message': 'Logout successful'}), 200

# Profile endpoint
@app.route('/profile', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    if 'username' in session:
        return jsonify({'username': session['username'], 'email': session['email']}), 200
    else:
        return jsonify({'message': 'User not logged in'}), 401