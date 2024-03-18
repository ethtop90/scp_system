from app import app, mongo, bcrypt
import requests, json
from flask import Flask, jsonify, Blueprint
from pathlib import Path
from datetime import datetime, timedelta
from bson import ObjectId

from models.scp_setting import Scp_setting
from apscheduler.schedulers.background import BackgroundScheduler
import config
from utils.wp_post.crud import *
schedules = []
auto_system_scheduler = BackgroundScheduler()

def autosystem():
    global schedules, auto_system_scheduler
    # auto_system_scheduler = BackgroundScheduler()
    import_schedules()
    for schedule in schedules:
        # auto_system_scheduler.add_job(auto_post(schedule.get('id')), 'date', schedule.get('pt_start_time'))
        auto_system_scheduler.add_job(auto_post, args=(schedule.get('id'),), trigger='date', run_date=datetime.strptime(schedule.get('start_time'), "%Y-%m-%dT%H:%M"), id=schedule.get('id'))
    
    auto_system_scheduler.start()
    print(auto_system_scheduler.scheduled_job)
    
def import_schedules():
    global schedules
    settings_cursor = mongo.db.scp_settings.find({"enabled": True})
    
    for setting in settings_cursor:
        if setting.get('next_time') and is_datetime_after_now(setting.get('next_time')):
            schedules.append({'start_time': setting.get('next_time'), "id": str(setting.get('_id'))})
    
from datetime import datetime

def is_datetime_after_now(datetime_str, datetime_format="%Y-%m-%dT%H:%M"):
    try:
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
    except ValueError as e:
        print(f"Error parsing datetime string: {e}")
        return False
    
    # Get the current datetime
    now = datetime.now()
    
    # Compare the datetime object with the current datetime
    return datetime_obj > now

def auto_post(id):
    print(id, datetime.now())
    obj_id = ObjectId(id)
    
    scp_setting = mongo.db.scp_settings.find_one({'_id':obj_id})
    if not scp_setting:
        print("SCP setting not found")
        return
    
    

    # Schedule the first execution of the post submission logic
    submit_post_to_wordpress(scp_setting)

# Define the logic for submitting posts to WordPress here
def submit_post_to_wordpress(scp_setting):
    # Placeholder for post submission logic
    print(f"Submitting post for setting {id}...")
    # Logic to submit post goes here
    submit_post(str(scp_setting['_id']), scp_setting['username'],'chintai' if scp_setting['data_type'] == 'rental' else 'baibai')
    # After submission, calculate next_time and update in database
    update_next_time(scp_setting)
    
    # Register the next execution
    setting = mongo.db.scp_settings.find_one({"_id": ObjectId(scp_setting['_id'])})

    schedule_next_execution(setting)

def update_next_time(scp_setting):
    # Calculate the next execution time based on UP_SETTINGS
    up_settings = scp_setting['up_settings']
    week_check = scp_setting['week_check']
    current_time_str = scp_setting.get('next_time')
    current_time = datetime.strptime(current_time_str, "%Y-%m-%dT%H:%M")
    # Assuming current_time is a datetime object
    current_weekday = current_time.weekday()
    next_time = None
    
    for i in range(1, 8): # Check the next 7 days
        next_weekday = (current_weekday + i) % 7
        if week_check[next_weekday]: # If the day is enabled for posting
            next_time_str = up_settings[next_weekday]
            # next_time = datetime.strptime(next_time_str, "%H:%M").replace(year=current_time.year, month=current_time.month, day=current_time.day) + timedelta(days=i)
            next_time = current_time.replace(hour=int(next_time_str), minute=0, second=0, microsecond=0) + timedelta(days=i)
            break
    
    if next_time:
        next_time_str = next_time.strftime("%Y-%m-%dT%H:%M")
        # Update the database with the new next_time
        mongo.db.scp_settings.update_one({"_id": ObjectId(scp_setting['_id'])}, {"$set": {"next_time": next_time_str}})
    else:
        print("Could not calculate the next_time")

def schedule_next_execution(scp_setting):
    # This function schedules the next execution based on the updated NEXT_TIME
    next_time = scp_setting.get('next_time')
    id = str(scp_setting['_id'])
    if next_time:
        auto_system_scheduler.add_job(auto_post, args=(id,), trigger='date', run_date=datetime.strptime(next_time, "%Y-%m-%dT%H:%M"), id=id)
        print(auto_system_scheduler.get_jobs)
    else:
        print("NEXT_TIME is not set, cannot schedule next execution")
        
def submit_post(id, username, data_type):
    # get the required information--------------------
    
    # get the all data id is id-----
    post_all_data = mongo.db.scp_alldatas.find({'id': id})
    
    
    
    post_all_status = {}
    check_status(id, username, data_type, post_all_status)
    
    # get the all
    for post in post_all_data:
        
        if '_id' in post:
        # Remove the '_id' key from the document
            del post['_id']
        
        if post.get('data'):
            title = post.get('data').get('物件名称')
        else:
            title = None
            
        if post_all_status.get(title):
            status = post_all_status.get(title).get('status')
        else:
            status = None
            
        if status != "trash":
            wp_post_add(data_type, title, status, post.get('data'), post_all_status.get(title).get('id') if post_all_status.get(title) else None)
        
def check_status(id, username, data_type, post_all_status):
    # get the draft posts -------------------------------------------------------
    # Base URL of your WordPress site's REST API
    base_url = config.wp_url+ "wp-json/wp/v2/" + data_type
    user_id = mongo.db.wp_users.find_one({'username': username})
    auth = (config.admin, config.application_password)
    # Send GET request to the WordPress REST API
    response = requests.get(base_url, auth=auth)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response JSON data
        data = response.json()
        
        # Extract id and title from each element and append to result list
        for item in data:
            post_all_status[str(item["title"]["rendered"])] = {
                "id": item["id"],
                "title": item["title"]["rendered"],
                "status": item["status"]
            }
        print(post_all_status)
    else:
        print("Failed to retrieve posts:", response.status_code)

    # get the draft posts -------------------------------------------------------
    base_url = config.wp_url+ "wp-json/wp/v2/" + data_type + "?status=draft"
    user_id = mongo.db.wp_users.find_one({'username': username})
    auth = (config.admin, config.application_password)
    # Send GET request to the WordPress REST API
    response = requests.get(base_url, auth=auth)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response JSON data
        data = response.json()
        
        # Extract id and title from each element and append to result list
        for item in data:
            post_all_status[str(item["title"]["rendered"])] = {
                "id": item["id"],
                "title": item["title"]["rendered"],
                "status": item["status"]
            }
        print(post_all_status)
    else:
        print("Failed to retrieve posts:", response.status_code)
        
    # get the draft posts -------------------------------------------------------
    base_url = config.wp_url+ "wp-json/wp/v2/" + data_type + "?status=trash"
    user_id = mongo.db.wp_users.find_one({'username': username})
    auth = (config.admin, config.application_password)
    # Send GET request to the WordPress REST API
    response = requests.get(base_url, auth=auth)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response JSON data
        data = response.json()
        
        # Extract id and title from each element and append to result list
        for item in data:
            post_all_status[str(item["title"]["rendered"])] = {
                "id": item["id"],
                "title": item["title"]["rendered"],
                "status": item["status"]
            }
        print(post_all_status)
    else:
        print("Failed to retrieve posts:", response.status_code)
        
    

if __name__ == '__main__':
    check_status(None, '5rfujikawa', 'selling', [])