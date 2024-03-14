import requests

# The URL of your WordPress login page
login_url = 'https://ymgfg.co.jp/wp-login.php'

# Replace 'yourusername' and 'yourpassword' with your WordPress login credentials
payload = {
    'log': '5rfujikawa',  # Username
    'pwd': 'UV$PO8TkMEi^LPkQbtG#MRSA',  # Password
    'wp-submit': 'Login',
    'redirect_to': 'https://ymgfg.co.jp/wp-admin',
    'testcookie': '1'
}

with requests.Session() as session:
    # Send a POST request to the login URL with the payload
    response = session.post(login_url, data=payload)
    
    # Check if login was successful by looking for a redirect to the admin area
    if 'wp-admin' in response.url:
        print("Login successful!")
        # You can now make further requests with the session object, and they will be authenticated
    else:
        print("Login failed. Check your username and password.")
