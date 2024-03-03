from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId
import pandas as pd
import os
import json

# import models
from models.user import User
from models.scp_setting import Scp_setting
from models.scp_url import Scp_url
from models.matching_data import Matching_data
from models.sit

# import utils
from utils.search_engine import create_mapping

UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


scp_running = Blueprint('scp-running', __name__)


@scp_running.route('/get-data/file', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def get_data_from_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(file.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # get the parameter from request
        # source = request.args.get('source')

        mapping, item_keys, first_data = import_data_from_file(filepath)
        item_keys_list = list(item_keys)

        result = {
            "mapping": mapping,
            "item_keys": item_keys_list,
            "first_data": first_data
        }
        return jsonify(result)

        # return jsonify({'success': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})

# route for scrapping


@scp_running.route('/get-data/site', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def get_data_from_url():
    setting = request.get_json()
    mapping, item_keys, valid = import_data_from_site(setting['source'])
    result = {
        "mapping": mapping,
        "item_keys": item_keys,
        "valid": True
    }
    return jsonify(result)


# -----

# get the matching_data
@scp_running.route('/matching-data/get', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def matching_data_get():
    username = request.args.get('username')
    id = request.args.get('id')

    data = mongo.db.matching_datas.find_one(
        {'$and': [{'username': username}, {'id': id}]})
    print(data)
    data_obj = Matching_data(
        data.get("username"),
        data.get("id"),
        data.get("first_data"),
        data.get("item_keys"),
        data.get("mapping")
    )

    return jsonify(data_obj.__dict__)

# -----

# get the matching_data


@scp_running.route('/matching-data/add', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def matching_data_add():
    username = request.args.get('username')
    id = request.args.get('id')
    # obj_id = ObjectId(id)
    data = request.get_json()
    data['id'] = id
    data['username'] = username
    query = {'$and': [{'username': username}, {'id': id}]}

    searchResult = mongo.db.matching_datas.find_one(
        query)

    if not searchResult:
        result = mongo.db.matching_datas.insert_one(data)

    else:
        result = mongo.db.matching_datas.update_one(query, {'$set': data})

    if result.acknowledged:
        return jsonify({'message': 'matching setting added successfully'})
    else:
        return jsonify({'message': 'Failed to matching setting'})

# -----

# get the matching_data


@scp_running.route('/matching-data/delete-item', methods=['DELETE'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def matching_data_delete():
    username = request.args.get('username')
    id = request.args.get('id')
    # obj_id = ObjectId(id)
    data = request.get_json()
    data['id'] = id
    data['username'] = username
    query = {'$and': [{'username': username}, {'id': id}]}

    result = mongo.db.matching_data.delete_one(query)

    if result.deleted_count == 1:
        return jsonify({'message': 'matching setting deleted successfully'})
    else:
        return jsonify({'message': 'Failed to matching setting'})

# -----

    # function import from excel file


def import_data_from_file(source):
    if is_valid_source(source) is False:
        return False

    # Read the Excel file into a pandas DataFrame
    xfile = pd.read_excel(source)
    json_data = xfile.to_json(orient='records')
    data_dic = json.loads(json_data)
    # print(json_data)
    # final_json_data = json.dumps(json.loads(json_data), ensure_ascii=False, default=str)
    # print(final_json_data)
    # return final_json_data
    keys = data_dic[0].keys()
    # print(keys)
    return (match_keys(keys), keys, data_dic[0])

# -----

# funtion keys of .xlse file and default keys


def match_keys(request_key_list):
    origin_keys = mongo.db.yamaguchi_data_keys.find_one({
        "type": "default"
    })

    distinct_keys = origin_keys['matches']
    origin_key_list = list(distinct_keys) if distinct_keys else []

    mapping = create_mapping(request_key_list, origin_key_list)

    print(mapping)
    return mapping

# ----


# function import from site url
def import_data_from_site(url):
    result = mongo.db.scp_urls.find_one({"url": url})
    
    mapping = None
    item_keys = None
    valid = None
    if not result.acknowledged:
        return (None, None, False)
    
    

    # running scrape function
    print(scp_function(url))
    return (mapping, item_keys,valid)  # three arguments
# -----

# function scrape from site


def scp_function(url):
    site_structure_cursor = mongo.db.site_structures.find_ond({"url": url})


    site_structure 


    return True
# -----

# function check if it is valid source


def is_valid_source(source):
    return os.path.exists(source)

# -----


app.register_blueprint(scp_running, url_prefix="/scp-running")
