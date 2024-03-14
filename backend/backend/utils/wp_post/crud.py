import requests, json
from flask import Flask, jsonify, Blueprint

base_url = "https://ymgfg.co.jp//wp-json/wp/v2/"

with open('../../base_data/post_field_baibai.json', 'r') as file:
    baibai_data = json.loads(file)
    
with open('../../base_data/post_field_chintai.json', 'r') as file:
    chintai_data = json.loads(file)
    
def post_add(data_type, username, application_password, title, status, post_field_data):
    if data_type == 'chintai':
        field_dictionary = chintai_data
    else: 
        field_dictionary = baibai_data 
        
    post_field_data = request.get_json() #array {'field_name': value, ...}
    
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

