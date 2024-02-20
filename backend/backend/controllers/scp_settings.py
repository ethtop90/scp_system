#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import modules
from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId

# import models
from models.user import User
from models.scp_setting import Scp_setting

scp_settings = Blueprint('scp-settings', __name__)


# geting all scraping settings

@scp_settings.route('/getall', methods=['GET'])
def getall():
    # getting the username

    username = request.args.get('username')
    user = mongo.db.users.find_one(
        {'username': username})  # check if user's existance
    if not user:
        return jsonify({'error': 'Unregisterd user!'}), 404
    # import user's scraping settings
    scp_settings_cursor = mongo.db.scp_settings.find({'username': username})
    
    # Convert the cursor to a list
    scp_settings_list = [
        {**item, "_id": str(item["_id"])}  # Convert ObjectId to string
        for item in scp_settings_cursor
    ]
    
    # Use bson.json_util.dumps for proper serialization
    serialized_settings = dumps(scp_settings_list, ensure_ascii=False)
    print(serialized_settings)
    
    return jsonify(serialized_settings)
#-----

# getting one scraping setting

@scp_settings.route('/get-item', methods=['GET'])
def get_item():
    # getting the username, type, source

    username = request.args.get('username')
    # type = request.args.get('type')
    id = request.args.get('id')
    # if type is "site":
    #     site_url = request.args.get('source')
    # else:
    #     file_path = request.args.get('source')
    obj_id = ObjectId(id)
    user = mongo.db.users.find_one(
        {'username': username})  # check if user's existance
    if not user:
        return jsonify({'error': 'User not found'}), 404
    scp_setting = mongo.db.scp_settings.find_one(
        {'$and': [{'username': username}, {'_id':obj_id}]})  # import user's scraping settings
    scp_setting_obj = Scp_setting(
        str(scp_setting["_id"]),
        scp_setting.get("type"),
        scp_setting.get("mg_title"),
        scp_setting.get("pt_name"),
        scp_setting.get("source"),
        scp_setting.get("username")
    )
    print(scp_setting_obj)
    return jsonify(scp_setting_obj.__dict__)
# -----


# updating one scraping setting

@scp_settings.route('/update-item', methods=['put'])
def update_item():
    # getting the username, type, source
    username = request.args.get('username')
    id = request.args.get('id')
    new_setting_data  = request.get_json()

    #updating the scraping setting data
    obj_id = ObjectId(id)
    query = {'$and': [{'username': username}, {'_id':obj_id}]}
    scp_setting = mongo.db.scp_settings.find_one(query)
    if not scp_setting:
        return jsonify({'message': 'Not found the scrapping system'})
    result = mongo.db.scp_settings.update_one(query, {'$set': new_setting_data})
    if result.acknowledged:
        return jsonify({'message': 'Scraping setting updated successfully'})
    else:
        return jsonify({'message': 'Failed to scraping updating'})
#-----


# adding one scraping setting

@scp_settings.route('/add-item', methods=['post'])
def add_item():
    #getting the username
    username = request.args.get('username')
    new_setting_data = request.get_json()

    #adding the scraping setting data to getted user
    query = {'username': username}
    new_setting_data['username'] = username
    result = mongo.db.scp_settings.insert_one(new_setting_data)

    if result.acknowledged:
        return jsonify({'message': 'Scraping setting added successfully'})
    else:
        return jsonify({'message': 'Failed to scraping setting'}) 
#-----
    

# deleting one scraping setting
    
@scp_settings.route('/delete-item', methods = ['delete'])
def delete_item():
    #getting the username, id
    username = request.args.get('username')
    id = request.args.get('id')

    #deleteing the scraping setting
    obj_id = ObjectId(id)
    query = {'$and': [{'username': username}, {'_id':obj_id}]}
    scp_setting = mongo.db.scp_settings.find_one(query)
    if not scp_setting:
        return jsonify({'message': 'Not found the scrapping system'})
    result = mongo.db.scp_settings.delete_one(query)
    return {'message': 'Scraping setting updated successfully'}
#-----

#register the blueprint


app.register_blueprint(scp_settings, url_prefix="/scp-settings")
#-----

def is_valid_object_id(obj_id):
    try:
        # Attempt to create an ObjectId with the given string
        ObjectId(obj_id)
        return True
    except:
        # An exception will be raised if the ObjectId is not valid
        return False