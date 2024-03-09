from app import mongo, bcrypt

db = mongo.db

class Scp_setting:
    def __init__(self, id, username, type, data_type, mg_title, pt_name, source, pt_start_time, week_check, up_settings):
        self.id = id
        self.username = username
        self.type = type # site|file
        self.data_type = data_type
        self.mg_title = mg_title
        self.pt_name = pt_name
        self.source = source
        self.pt_start_time = pt_start_time
        self.up_settings = up_settings
        self.week_check = week_check