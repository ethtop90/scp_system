import requests
import config
from requests.auth import HTTPBasicAuth

# The base URL of your WordPress site's REST API
def get_user_list(username):
        
    base_url = "https://ymgfg.co.jp/wp-json"

    # Endpoint for retrieving users
    endpoint = "/wp/v2/users"

    # Complete URL
    url = base_url + endpoint

    # Your WordPress username and application password
    username = config.admin
    application_password = config.application_password
    # Make the GET request with Basic Authentication
    response = requests.get(url, auth=HTTPBasicAuth(username, application_password))
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        users = response.json()
    else:
        return None, None, None
    
    user = next((user for user in users if user['name'] == username), None)
    

    return users, user['id'], None

# def get_application_password(user_id):
#     endpoint = config.wp_url + f'/wp-json/wp/v2/users/{user_id}/application-passwords'
#     response = requests.get(config.wp_url + endpoint)
#     application_password = response.data
#     return application_password
