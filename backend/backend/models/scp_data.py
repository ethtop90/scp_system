from app import mongo, bcrypt

db = mongo.db

class scp_data:
    def __init__(self, type, company_name, site_url, list_base_url, is_page, pg_param, total_cnt_rex,limit_param, limit, data_structure):
        self.id = id
        self.type = type
        self.company_name = company_name
        self.site_url = site_url
        self.list_base_url = list_base_url
        self.is_page = is_page
        self.pg_param = pg_param
        self.total_cnt_rex = total_cnt_rex
        self.limit_param = limit_param
        self.limit = limit
        self.data_structure = data_structure