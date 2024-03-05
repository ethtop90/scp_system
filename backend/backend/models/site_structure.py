from app import mongo, bcrypt
from mongoengine import Document, StringField

db = mongo.db

class Site_structure:
    def __init__(self, type, company_name, site_url, is_seperate, seperated_pages,list_base_url, is_pagination, link_rex, page_limit_exist, pg_param, total_cnt_rex, limit_param, limit, data_structure):
        self.type = type
        self.company_name = company_name
        self.site_url = site_url
        self.is_seperate = is_seperate
        self.seperated_pages = seperated_pages
        self.list_base_url = list_base_url
        self.is_pagination = is_pagination
        self.link_rex = link_rex
        self.page_limit_exist = page_limit_exist
        self.pg_param = pg_param
        self.total_cnt_rex = total_cnt_rex
        self.limit_param = limit_param
        self.limit = limit
        # self.data_structure = Data_structure(**data_structure)
        self.data_structure = Data_structure(**data_structure)

class Data_structure:
    def __init__(self, image_source_rex, table_data_structure, map_rex):
        self.image_source_rex = image_source_rex
        self.table_data_structure = Table_data_structure(**table_data_structure)
        self.map_rex = map_rex

class Table_data_structure:
    def __init__(self, table_entire_rex, tr_rex, th_rex, td_rex):
        self.table_entire_rex = table_entire_rex
        self.tr_rex = tr_rex
        self.th_rex = th_rex
        self.td_rex = td_rex