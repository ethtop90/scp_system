from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId
import pandas as pd
import os
import json
import config
import requests, re

# import models
from models.user import User
from models.scp_setting import Scp_setting
from models.scp_url import Scp_url
from models.matching_data import Matching_data
from models.site_structure import Site_structure
from models.scp_alldata import Scp_alldata

from utils.scp_system import scp_system
from utils.wp_post_template import *
from utils.wp_post.crud import *

# import utils
from utils.search_engine import create_mapping
from utils.taxonomi_excel_handler import taxonomi_babai, taxonomi_chintai

get_type =  'one'

UPLOAD_FOLDER = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


scp_running = Blueprint('scp-running', __name__)

@scp_running.route('/get-data/site', methods=['GET'])
def scp_running_getdata_site_index():
    return app.send_static_file('index.html')

@scp_running.route('/get-data/file', methods=['GET'])
def scp_running_gedata_file_index():
    return app.send_static_file('index.html')


@scp_running.route('/get-data/file', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def get_data_from_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    type = request.args.get('type')
    file = request.files['file']
    get_type = request.args.get('get_type')
    

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(file.filename)

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # get the parameter from request
        # source = request.args.get('source')
        if get_type == 'one':
            mapping, item_keys, all_data, valid = import_data_from_file(filepath, type)
            item_keys_list = list(item_keys)

            result = {
                "mapping": mapping,
                "item_keys": item_keys_list,
                "first_data": all_data[0],
                "valid": valid
            }
        else:
            mapping, item_keys, all_data, valid = import_data_from_file(filepath, type)
            item_keys_list = list(item_keys)

            result = {
                "mapping": mapping,
                "item_keys": item_keys_list,
                "all_data": all_data,
                "valid": valid
            }
            
        return jsonify(result)

        # return jsonify({'success': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})

# route for scrapping


@scp_running.route('/get-data/site', methods=['POST'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def get_data_from_url():
    global get_type
    get_type = request.args.get('get_type')
    type = request.args.get('type')
    setting = request.get_json()
    config.global_scp_method = False
    if get_type == 'one':
        first_data, mapping, item_keys, valid = import_data_from_site(setting['source'], type)
        result = {
            "mapping": mapping,
            "item_keys": item_keys,
            "first_data": first_data.table,
            "first_images": first_data.images,
            "first_map_link": first_data.map_link,
            "valid": valid
        }
    else:
        all_data, mapping, item_keys, valid = import_data_from_site(setting['source'], type)
        all_table_data = []
        all_images = []
        all_map_link = []
        for data in all_data:
            all_table_data.append(data.table)
            all_images.append(data.images)
            all_map_link.append(data.map_link)
        result = {
            "mapping": mapping,
            "item_keys": item_keys,
            "all_data": all_table_data,
            "all_images": all_images,
            "all_map_link": all_map_link,
            "valid": valid
        }
    return jsonify(result)


# -----

# get the matching_data
@scp_running.route('/matching-data/get', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def matching_data_get():
    username = request.args.get('username')
    id = request.args.get('id')
    type = request.args.get('type')

    data = mongo.db.matching_datas.find_one(
        {'$and': [{'username': username}, {'id': id}]})

    if data:
        data_obj = Matching_data(
            data.get("username"),
            data.get("id"),
            data.get("first_data"),
            data.get("item_keys"),
            data.get("mapping")
        )
        data_dict = data_obj.to_dict()
    else:
        data_dict = None

    return jsonify(data_dict)

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

    result = mongo.db.matching_datas.delete_one(query)

    if result.deleted_count == 1:
        return jsonify({'message': 'matching setting deleted successfully'})
    else:
        return jsonify({'message': 'Failed to matching setting'})

# -----

    # function import from excel file


def import_data_from_file(source, type):
    # if is_valid_source(source) is False:
    #     return False

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
    return (match_keys(keys, type), keys, data_dic, True)

# -----

# funtion keys of .xlse file and default keys


def match_keys(request_key_list, type):
    origin_keys = mongo.db.yamaguchi_data_keys.find_one({
        "type": type
    })
    print(type)

    distinct_keys = origin_keys['matches']
    origin_key_list = list(distinct_keys) if distinct_keys else []

    mapping = create_mapping(request_key_list, origin_key_list)

    print(mapping)
    return mapping

# ----


# function import from site url
def import_data_from_site(url, type):
    # result = mongo.db.scp_urls.find_one({"url": url})
    global get_type
    result = mongo.db.site_structures.find_one({'$and': [{'site_url': url}, {'type': type}]})

    
    mapping = None
    item_keys = None
    valid = None
    if result is None:
        return (None,None, None, False)
    
    

    # running scrape function
    if get_type == 'one':
        first_data, valid = scp_function(url, type)
        request_keys = list(first_data.table.keys())
        mapping = match_keys(request_keys, type)

        return (first_data, mapping, request_keys,valid)  # three arguments
    else:
        all_data, valid = scp_function(url, type)

        return (all_data, None, None, True)
# -----

# function scrape from site

def get_value_or_none(obj, key):
    if key in obj:
        return obj.get(key)
    else:
        return None

def scp_function(url, type):
    global get_type
    site_structure_cursor = mongo.db.site_structures.find_one({'$and': [{'site_url': url}, {'type': type}]})
    if not site_structure_cursor:
        return {}, False 
    site_structure_cursor.pop('_id')

    # site_structure = Site_structure(**site_structure_cursor)
    try:
        site_structure = Site_structure(
            type=get_value_or_none(site_structure_cursor, 'type'),
            company_name=get_value_or_none(site_structure_cursor, 'company_name'),
            site_url=get_value_or_none(site_structure_cursor, 'site_url'),
            is_seperate=get_value_or_none(site_structure_cursor, 'is_seperate'),
            seperated_pages=get_value_or_none(site_structure_cursor, 'seperated_urls'),
            list_base_url=get_value_or_none(site_structure_cursor, 'list_base_url'),
            is_pagination=get_value_or_none(site_structure_cursor, 'is_pagination'),
            link_rex=get_value_or_none(site_structure_cursor, 'link_rex'),
            page_limit_exist=get_value_or_none(site_structure_cursor, 'page_limit_exist'),
            pg_param=get_value_or_none(site_structure_cursor, 'pg_param'),
            total_cnt_rex=get_value_or_none(site_structure_cursor, 'total_cnt_rex'),
            limit_param=get_value_or_none(site_structure_cursor, 'limit_param'),
            limit=get_value_or_none(site_structure_cursor, 'limit'),
            data_structure=get_value_or_none(site_structure_cursor, 'data_structure')
        )
        print(site_structure)
        datas = scp_system(site_structure, get_type)
        if len(datas) and (get_type == 'one'):
            return datas[0], True
        else:
            return datas, True
        return none
    except Exception as e:
        print(f"Error creating Site_structure instance: {e}")
    
# -----


# function check if it is valid source


def is_valid_source(source):
    return os.path.exists(source)

# -----

@scp_running.route('/save-alldata', methods=['POST'])
def scp_running_save_alldata():
    username = request.args.get('username')
    id = request.args.get('id')
    data_type = request.args.get('dataType')
    all_data = request.get_json()['data']
    all_data = all_data[1:]
    
    for index, item_data in enumerate(all_data):
        
        if filter_by_taxonomi(item_data, data_type) is False:
            continue
        update_data = {} 
        update_data['id'] = id
        update_data['username'] = username
        update_data['data'] = item_data
        update_data['data_type'] = data_type
        # update_data['images'] = item_data.get('images')
        # update_data['map_link'] = item_data.get('map_link')
        if update_data['data'].get('物件名称') is None:
            update_data['title'] = str(username + id + str(index))
        else:
            update_data['title'] = update_data['data'].get('物件名称')
        query = {'$and': [{'username': username}, {'id': (id)}, {'title': update_data['title']}]}
        searchResult = mongo.db.scp_alldatas.find_one(
            query)
        
        

        if not searchResult:
            result = mongo.db.scp_alldatas.insert_one(update_data)

        else:
            result = mongo.db.scp_alldatas.update_one(query, {'$set': update_data})
    return {'message': 'Data are stored successfully in database'}

def filter_by_taxonomi(item, data_type):
    # dic = taxonomi_babai if data_type == "selling" else taxonomi_chintai
    # for key, value in item.items():
        
    #     if (value is not None) and (key in dic) and (len(dic.get(key)) > 0):
    #         if value in dic.get(key):
                
    #             continue
    #         else:
    #             return False
    return True

# @scp_running.route('/post-to-wp', methods=['POST'])
# @cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
# def wp_post_alldata():
#     data_type = request.args.get('dataType')
#     username = request.args.get('username')
#     status = request.args.get('status')
#     id = request.args.get('id')
#     application_password = request.args.get('application_password')
#     request_data = request.get_json()
#     all_data = request.get_json()['data']
#     all_data = all_data[1:]
    
#     for index, item_data in enumerate(all_data):
#         if item_data.get('物件名称') is None:
#             title = username + id + index
#         else:
#             title = item_data.get('物件名称')
#         #get post_id
#         post_add(data_type, username, application_password, title, status, item_data)
#     return jsonify({'messsage': 'articles are posted successfully'})

app.register_blueprint(scp_running, url_prefix="/scp-running")
