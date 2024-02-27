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

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

scp_running = Blueprint('scp-running', __name__)

@scp_running.route('/get-data/file', methods=['POST'])
def get_data_from_file():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(filepath))

        #get the parameter from request
        type = request.args.get('type')
        # source = request.args.get('source')

        result = import_data_from_file(filepath) # result is json
        
        return jsonify(result)

        # return jsonify({'success': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})
    
# route for scrapping
@scp_running.route('/get-data/url', methods=['POST'])
def get_data_from_url():
    setting = request.get_json()
    # print("url:", setting['source'])
    result = import_data_from_site(setting['source'])
    if result is True:
        return jsonify({"message": "scraped unsuccessfully"})
    return jsonify(result)


#-----
    
# function import from excel file
def import_data_from_file(source):
    if is_valid_source(source) is False:
        return False

    # Read the Excel file into a pandas DataFrame
    xfile = pd.read_excel(source)
    json_data = xfile.to_json(orient='records')
    final_json_data = json.dumps(json.loads(json_data), ensure_ascii=False, default=str)
    # print(final_json_data)
    return final_json_data

#-----


# function import from site url
def import_data_from_site(url):
    if is_valid_url(url) is False:
        return False
    # running scrape function
    print(scp_function(url))
#-----

#function scrape from site
def scp_function(url):
    return True
#-----
    
#function check if it is valid source
def is_valid_source(source):
    return os.path.exists(source)
    

#-----
    
#function check if it is valid url
def is_valid_url(url):
    print("103:", url)
    result = mongo.db.scp_urls.find_one({"url": url})
    if result is not None:
        return True
    else :
        return False

#-----




app.register_blueprint(scp_running, url_prefix="/scp-running")
