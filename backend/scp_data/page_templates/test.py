import requests
def check_status(id, username, data_type, post_all_status):
    # Base URL of your WordPress site's REST API
    base_url = 'https://ymgfg.co.jp/'+ "wp-json/wp/v2/property_chintai" + "/?status=trash"
    base_url = 'https://ymgfg.co.jp/'+ "wp-json/wp/v2/property_chintai" + "/?status=trash"
    # user_id = mongo.db.wp_users.find_one({'username': username})
    auth = (username, "c07p fp3D CVkv imIU f4ID RbIw")
    # Send GET request to the WordPress REST API
    response = requests.get(base_url, auth=auth)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response JSON data
        data = response.json()
        
        # Extract id and title from each element and append to result list
        for item in data:
            post_all_status.append({
                "id": item["id"],
                "title": item["title"]['rendered'],
                "status": item["status"]
            })
            print(item)
        # print(post_all_status)
    else:
        print("Failed to retrieve posts:", response.status_code)
        

if __name__ == '__main__':
    check_status(None, '5rfujikawa', 'baibai', [])