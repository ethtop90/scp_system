import requests
from requests.auth import HTTPBasicAuth

# The base URL of your WordPress site's REST API
base_url = "https://ymgfg.co.jp/wp-json"

# Endpoint for retrieving users
endpoint = "/wp/v2/users"

# Complete URL
url = base_url + endpoint

# Your WordPress username and application password
username = "5rfujikawa"
application_password = "c07p fp3D CVkv imIU f4ID RbIw"

# Make the GET request with Basic Authentication
response = requests.get(url, auth=HTTPBasicAuth(username, application_password))

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    users = response.json()
    # Print user information (example: IDs and names)
    for user in users:
        print(f"ID: {user['id']}, Name: {user['name']}")
else:
    print(f"Failed to retrieve users. Status code: {response.status_code}")
