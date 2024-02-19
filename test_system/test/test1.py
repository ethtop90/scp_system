# 1 site

from selenium import webdriver
import re
from urllib.parse import urljoin
import time
import json


# Assuming you have already initialized the webdriver (e.g., ChromeDriver)
driver = webdriver.Chrome()
home_url = "https://earth-fudosan.com";
base_url = "https://earth-fudosan.com/59896/";
driver.get(base_url)
# driver.get("https://www.urban-es.net/sale/result?r1=&r2=&t1=&t2=&n1=&n2=&tw=&tn=&fw=&rm_type=1&rm_per=&limit=90")

# Find links with "background-image" style
links = driver.find_elements('xpath',"//ul[@class='reals']//a[contains(@style, 'background-image')]")
images = set()
for link in links:
    images.add(link.get_attribute("style"))
print(images)
# # Print the href attribute of each link

for image in images:
    match = re.search(r'url\(["\'](.*?)["\']\)', image)
    re_url = match.group(1)

    ab_url = (urljoin(home_url, re_url))

hrefs = [link.get_attribute("href") for link in links]

cnt = 0
table_dic_cll = []

for item in hrefs:
    cnt = cnt + 1
    print(cnt)
    driver.get(item)
    time.sleep(2)
    tables = driver.find_elements('xpath', "//div[@class='tbl']//table")
    table_dic = {}
    for table in tables:
    # Find all rows in the table
        
        rows = table.find_elements("xpath", ".//tr")

        # Iterate through each row
        for row in rows:
            # Find th (header) and td (data) elements in the row
            headers = row.find_elements("xpath", ".//th")
            data_cells = row.find_elements("xpath", ".//td")

            # Extract text from th and td elements
            for header, data_cell in zip(headers, data_cells):
                x = header.text
                y = data_cell.text
                table_dic[x] = y;
                # print(f"x: {x}, y: {y}")
    table_dic_cll.append(table_dic)
table_json_data = json.dumps(table_dic_cll, ensure_ascii=False)
print(table_json_data)
# Don't forget to close the browser window when done
driver.quit()
