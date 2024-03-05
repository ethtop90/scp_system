from models import Site_structure
from app import mongo

def scp_function(url):
    site_structure_cursor = mongo.db.site_structures.find_one({"url": url})
    if not site_structure_cursor:
        return False
    site_structure_cursor.pop('_id')

    site_structure = Site_structure(**site_structure_cursor)
    scp_data =  scp_system(site_structure)



    return True
# -----
test_url = "https://earth-fudosan.com/"
scp_function(test_url)