from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from werkzeug.utils import secure_filename
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId
import pandas as pd
import os

# import models
from models.user import User
from models.scp_setting import Scp_setting

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

scp_running = Blueprint('scp-running', __name__)

@scp_running.route('/get-data', methods=['GET'])
def get_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)

        #get the parameter from request
        type = request.args.get('type')
        # source = request.args.get('source')

        if type == 'file':  #when type is file
            result = import_data(filename)
        else:   # when type is URL
            result = scp_function(filename)
        
        return jsonify(result)

        # return jsonify({'success': 'File uploaded successfully'})
    else:
        return jsonify({'error': 'Invalid file format'})
    
# function import from excel file
def import_data(source):
    if is_valid_source(source) is False:
        return False

    # Read the Excel file into a pandas DataFrame
    xfile = pd.read_excel(source)
    print(xfile)

#-----


#function scrape from site
def scp_function(source):
    is_valid_url(source)
#-----
    
#function check if it is valid source
def is_valid_source(source):
    return os.path.exists(source)
    

#-----
    
#function check if it is valid url
def is_valid_url(source):
    result = mongo.db.scp_urls.find_one({"url": source})
    
    if result.acknowledged:
        return True
    else :
        return False

#-----




app.register_blueprint(scp_running, url_prefix="/scp-running")
