import requests

url = "https://ymgfg.co.jp//wp-json/wp/v2/baibai"
auth = ("5rfujikawa", "XaIb D1FU oDYt ZdCe 2KKt uKsB")
headers = {"Content-Type": "application/json"}
data = {
    "title": "Your Post Title",
    "fields": {
        "property_name_baibai": "Value for ACF Field",
        "maximum_price_baibai": '2323'
    },
    "status": "publish"
}

response = requests.post(url, auth=auth, headers=headers, json=data)

print(response.text)  # Or handle the response as needed
