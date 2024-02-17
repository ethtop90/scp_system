#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, mongo, bcrypt
from flask import jsonify, request, session
from flask_cors import cross_origin
from models.user import User

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
        return jsonify({'message': 'Login successful','email':user['email']}), 200
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
def profile():
    if 'username' in session:
        return jsonify({'username': session['username'], 'email': session['email']}), 200
    else:
        return jsonify({'message': 'User not logged in'}), 401