import requests, json
from flask import Flask, jsonify, Blueprint
from pathlib import Path

base_path = Path(__file__).parent

base_url = "https://ymgfg.co.jp//wp-json/wp/v2/"

with open(base_path / '../../base_data/post_field_baibai.json', 'r', encoding='utf-8') as file:
    baibai_data = json.load(file)
    
with open(base_path / '../../base_data/post_field_chintai.json', 'r', encoding='utf-8') as file:
    chintai_data = json.load(file)
    
def post_add(data_type, username, application_password, title, status, post_field_data):
    data_type = "chintai" if data_type == 'rental' else "baibai"
    if data_type == 'chintai':
        field_dictionary = chintai_data
    else: 
        field_dictionary = baibai_data 
         #array {'field_name': value, ...}
    
    url = base_url + data_type
    
    auth = (username, application_password)
    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "fields": {  # Initialize the "fields" dictionary
            # Add all values from post_field_data to "fields"
            field_dictionary[field_name].get('field_name'): value for field_name, value in post_field_data.items()
        },
        "status": status
    }
    

    response = requests.post(url, auth=auth, headers=headers, json=data)

    if response.ok:
        return True
    else:
        return False

