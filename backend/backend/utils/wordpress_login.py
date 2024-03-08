import requests, time
from selenium import webdriver


url = 'https://ymgfg.co.jp/wp-login.php'

def wordpress_login(username, password):
    payload = {
        'log': username,
        'wp-submit': 'ログイン',
        'redirect_to': 'https://ymgfg.co.jp/wp-admin/',
        'testcookie': '1',
        'pwd': password
    }
    
    response = requests.post(url, data=payload)

    # Handle the response
    if response.status_code == 200:
        # Handle the successful response
        cookies = response.cookies.get_dict()
        
        # Open Chrome browser and set cookies
        driver = webdriver.Chrome()
        driver.get("https://ymgfg.co.jp/wp-admin/")
        for cookie in cookies:
            driver.add_cookie({
                'name': cookie,
                'value': cookies[cookie]
            })
        driver.get("https://ymgfg.co.jp/wp-admin/")
        time.sleep(20)
    else:
        print('Error:', response.status_code)
   
# test method
def test():
    wordpress_login('5rfujikawa', 'UV$PO8TkMEi^LPkQbtG#MRSA')
    
test()
