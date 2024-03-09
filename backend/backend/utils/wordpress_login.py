import requests, time
from selenium import webdriver
import config
import json

url = config.wp_url + 'wp-login.php'

def wordpress_login(username, password):
    payload = {
        'log': username,
        'wp-submit': 'ログイン',
        'redirect_to': config.wp_url + 'wp-admin/',
        'testcookie': '1',
        'pwd': password
    }
    
    response = requests.post(url, data=payload)
    
    # Handle the response
    if response.status_code == 200:
        print("wp-login is proceed successfully")
        # Handle the successful response
        cookies = response.cookies.get_dict()
        
        serialize_cookies = json.dumps(cookies)
        return serialize_cookies
    else:
        print('Error:', response.status_code)
        return None