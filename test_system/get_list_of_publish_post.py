import requests, json
from flask import Flask, jsonify, Blueprint
from pathlib import Path



base_path = Path(__file__).parent

base_url = "https://ymgfg.co.jp/wp-json/wp/v2/"
data_type = 'chintai'
username = '5rfujikawa'
application_password = "c07p fp3D CVkv imIU f4ID RbIw"

def check_published_post():
    url = base_url + data_type
    auth = (username, application_password)
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, auth=auth, headers=headers)
    if response.ok:
        content = json.loads(response._content.decode('utf-8'))
        return True, id
    else:
        return False, None
    
if __name__ == "__main__":
    check_published_post()