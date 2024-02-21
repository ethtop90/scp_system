from app import app, mongo, bcrypt
from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from bson.json_util import dumps
from bson import ObjectId
from pandas import pd

# import models
from models.user import User
from models.scp_setting import Scp_setting

scp_settings = Blueprint('scp-running', __name__)

@app.route('/get-data', method=['GET'])
def get_data():

    #get the parameter from request
    type = request.args.get('type')
    source = request.args.get('source')

    if type is 'file':  #when type is file
        import_data(source)
    else:   # when type is URL
        scp_function(source)

# function import from excel file
def import_data(source):
    if is_valid_source(source) is False:
        return False
    # Specify the path to your Excel file
    excel_file_path = 'path/to/your/file.xlsx'

    # Read the Excel file into a pandas DataFrame
    xfile = pd.read_excel(excel_file_path)

#-----


#function scrape from site
def scp_function():
    is_valid_url(source)
#-----
    
#function check if it is valid source
def is_valid_source(source):


#-----
    
#function check if it is valid url
def is_valid_url(source):
    

#-----




app.register_blueprint(scp_settings, url_prefix="/scp-settings")
