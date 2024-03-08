from app import app
from utils.wordpress_login import wordpress_login
from flask import request

@app.route('/wp-login', methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    wordpress_login(username, password)