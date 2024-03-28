from app import app, mongo, bcrypt
import requests, json
from flask import Flask, jsonify, Blueprint
from pathlib import Path

from models.scp_setting import Scp_setting
import config


base_path = Path(__file__).parent

base_url = "https://ymgfg.co.jp//wp-json/wp/v2/"


with open(base_path / '../../base_data/post_field_baibai.json', 'r', encoding='utf-8') as file:
    baibai_data = json.load(file)
    
with open(base_path / '../../base_data/post_field_chintai.json', 'r', encoding='utf-8') as file:
    chintai_data = json.load(file)
    
def wp_post_add(data_type, title, status, post_field_data, id):
    data_type = "chintai" if data_type == 'rental' else "baibai"
    if data_type == 'chintai':
        field_dictionary = chintai_data
    else: 
        field_dictionary = baibai_data 
         #array {'field_name': value, ...}
    
    url = base_url + data_type
    # url = base_url + '/posts'
    
    auth = (config.admin, config.application_password)
    headers = {"Content-Type": "application/json"}
    data = {
        "title": title,
        "acf": {  # Initialize the "fields" dictionary
            # Add all values from post_field_data to "fields"
            field_dictionary[field_name].get('field_name'): value for field_name, value in post_field_data.items()
        },
        "status": status if status is not None else 'draft'
    }
    
    if status == None:
        response = requests.post(url, auth=auth, headers=headers, json=data)
        if response.ok:
            content = json.loads(response._content.decode('utf-8'))
            id = content.get('id')
            return True, id
        else:
            return False, None
        
    if status == 'draft' or status == 'publish':
        response = requests.post(url + "/" + str(id), auth=auth, headers=headers, json=data)
        if response.ok:
            content = json.loads(response._content.decode('utf-8'))
            id = content.get('id')
            return True, id
        else:
            return False, None

        
# def check_published_post():
#     post_type = 'baibai'
#     url = base_url + post_type + '/2631'
#     auth = (config.admin, config.application_password)
#     headers = {"Content-Type": "application/json"}

#     response = requests.get(url, auth=auth, headers=headers)
#     if response.ok:
#         published_posts = json.loads(response._content.decode('utf-8'))

#         # Process the published posts as needed
#         print(published_posts)
#         return published_posts
#     else:
#         print("Failed to retrieve published posts")
#         return None
    
# if __name__ == "__main__":
#     check_published_post()
