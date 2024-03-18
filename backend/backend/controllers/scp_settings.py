#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import modules
from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId
import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler


# import models
from models.user import User
from models.scp_setting import Scp_setting

from utils.wp_post.auto_system import *

scp_settings = Blueprint('scp-settings', __name__)

@scp_settings.route('/', methods=['GET'])
def scp_setting_index():
    return app.send_static_file('index.html')

@scp_settings.route('/scp-running', methods=['GET'])
def scp_running_index():
    return app.send_static_file('index.html')


# geting all scraping settings
@scp_settings.route('/getall', methods=['GET'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def getall():
    # getting the username

    username = request.args.get('username')
    # user = mongo.db.users.find_one(
    #     {'username': username})  # check if user's existance
    # if not user:
    #     return jsonify({'error': 'Unregisterd user!'}), 404
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
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
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
    # # user = mongo.db.users.find_one(
    #     {'username': username})  # check if user's existance
    # if not user:
    #     return jsonify({'error': 'User not found'}), 404
    scp_setting = mongo.db.scp_settings.find_one(
        {'$and': [{'username': username}, {'_id':obj_id}]})  # import user's scraping settings
    
    scp_setting_obj = Scp_setting(
        str(scp_setting.get("_id")),
        scp_setting.get("username"),
        scp_setting.get("type"),
        scp_setting.get("data_type"),
        scp_setting.get("mg_title"),
        scp_setting.get("pt_name"),
        scp_setting.get("source"),
        scp_setting.get("enabled"),
        scp_setting.get("pt_start_time"),
        scp_setting.get("week_check"),
        scp_setting.get("up_settings")
    )
    print(scp_setting_obj)
    return jsonify(scp_setting_obj.__dict__)
# -----


# updating one scraping setting

@scp_settings.route('/update-item', methods=['put'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def update_item():
    # getting the username, type, source
    username = request.args.get('username')
    id = request.args.get('id')
    new_setting_data  = request.get_json()

    update_data = {}

    if 'type' in new_setting_data:
        update_data['type'] = new_setting_data['type']
    if 'data_type' in new_setting_data:
        update_data['data_type'] = new_setting_data['data_type']
    if 'mg_title' in new_setting_data:
        update_data['mg_title'] = new_setting_data['mg_title']
    if 'pt_name' in new_setting_data:
        update_data['pt_name'] = new_setting_data['pt_name']
    if 'source' in new_setting_data:
        update_data['source'] = new_setting_data['source']
    if 'enabled' in new_setting_data:
        update_data['enabled'] = new_setting_data['enabled']
    if 'pt_start_time' in new_setting_data:
        update_data['pt_start_time'] = new_setting_data['pt_start_time']
        update_data['next_time'] = new_setting_data['pt_start_time']
    if 'up_settings' in new_setting_data:
        update_data['up_settings'] = new_setting_data['up_settings']
    if 'week_check' in new_setting_data:
        update_data['week_check'] =  new_setting_data['week_check']


    #updating the scraping setting data
    obj_id = ObjectId(id)
    query = {'$and': [{'username': username}, {'_id':obj_id}]}
    scp_setting = mongo.db.scp_settings.find_one(query)
    if not scp_setting:
        return jsonify({'message': 'Not found the scrapping system'})
    result = mongo.db.scp_settings.update_one(query, {'$set': update_data})
    
    if result.acknowledged:
        updated_docment = mongo.db.scp_settings.find_one(query)
        handle_next_time(updated_docment)        
        return jsonify({'message': 'Scraping setting updated successfully'})
    else:
        return jsonify({'message': 'Failed to scraping updating'})
#-----

def handle_next_time(updated_document):
    # check if job exists
    job = auto_system_scheduler.get_job(str(updated_document.get('_id')))
    if job:
        # Remove the job
        auto_system_scheduler.remove_job(job.id)
        
        auto_system_scheduler.add_job(auto_post, args=(str(updated_document.get('_id')),), trigger='date', run_date=datetime.strptime(updated_document.get('next_time'), "%Y-%m-%dT%H:%M"), id = job.id)
    else:
        print("Job with ID {job.id} does not exist.")
        auto_system_scheduler.add_job(auto_post, args=(str(updated_document.get('_id')),), trigger='date', run_date=datetime.strptime(updated_document.get('next_time'), "%Y-%m-%dT%H:%M"), id = str(updated_document.get('_id')))
        
    print(auto_system_scheduler.get_jobs())

# adding one scraping setting

@scp_settings.route('/add-item', methods=['post'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
def add_item():
    #getting the username
    username = request.args.get('username')
    type = request.args.get('type')
    source = request.args.get('source')
    new_setting_data = request.get_json()

    #adding the scraping setting data to getted user
    query = {'username': username}

    new_setting_data['username'] = username
    new_setting_data['pt_start_time'] = datetime.datetime.now()
    new_setting_data['next_time'] = new_setting_data['pt_start_time']
    print(datetime.datetime.now())
    new_setting_data['enabled'] = False
    new_setting_data['up_settings'] = [0] * 7
    new_setting_data['week_check'] = [False] * 7

    find_result = mongo.db.scp_settings.find_one({'$and': [{'username': username}, {'data_type':type}, {'source':source}]})
    if not find_result:
        result = mongo.db.scp_settings.insert_one(new_setting_data)
    else:
        return jsonify({'message': 'setting already exists'});
    print(str(result.inserted_id))

    if result.acknowledged:
        query = {'$and': [{'username': username}, {'_id':result.inserted_id}]}
        updated_docment = mongo.db.scp_settings.find_one(query)
        handle_next_time(updated_docment)
        return jsonify({'message': 'Scraping setting added successfully', 'id':str(result.inserted_id)})
    else:
        return jsonify({'message': 'Failed to scraping setting'}) 
#-----
    

# deleting one scraping setting
    
@scp_settings.route('/delete-item', methods = ['delete'])
@cross_origin(origin=app.config['MAIN_URL'], headers=['Content-Type', 'Authorization'])
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