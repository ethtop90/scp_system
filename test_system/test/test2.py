# 1 site

from selenium import webdriver
import re
from urllib.parse import urljoin
import time
import json
import math


# Assuming you have already initialized the webdriver (e.g., ChromeDriver)
driver = webdriver.Chrome()
home_url = "https://www.urban-es.net/";
base_url = "https://www.urban-es.net/rent/result?r1=&r2=&t1=&t2=&tw=&tn=&td=&et=&fw=";
driver.get(base_url)
# driver.get("https://www.urban-es.net/sale/result?r1=&r2=&t1=&t2=&n1=&n2=&tw=&tn=&fw=&rm_type=1&rm_per=&limit=90")

# Find links with "background-image" style
list_base_url = "//div[@class='result-item']//div[@class='main-item']//a[@class='img']"
pg_param = "page" #pg_param
limit_param = "limit" #limi_param
limit = 90 
table_datas = ["//table[@class='table tableHead bkDetailDataHead']", "//table[@class='table table-bordered tableDetail']"]
tr_data = './/tr'
th_data = ".//th"
td_data = ".//td"


total_amount = driver.find_element("xpath", "//div[@class='bk-count']//span[@class='bundle']//span[@class='count']").text
print("total_amount:", total_amount)
# links = driver.find_elements('xpath',"")

pages_count = math.floor(int(total_amount) / limit) + 1;
page_urls = []
for i in range(1, pages_count + 1):
    page_url = base_url + "&" + f"{pg_param}={i}" + "&" + f"{limit_param}=90"
    print(page_url)
    page_urls.append(page_url)

table_dic_cll = []
for page_url in page_urls:
    driver.get(page_url)

    # getting the link elements
    links = driver.find_elements('xpath', list_base_url)

    #getting the hrefs
    hrefs = []
    hrefs = [link.get_attribute("href") for link in links]

    cnt = 0

    for item in hrefs:
        cnt = cnt + 1
        print(cnt)
        driver.get(item)
        time.sleep(1)

        tables = []
        for table_data in table_datas:
            one_table_group = driver.find_elements('xpath', table_data)
            for table in one_table_group:
                tables.append(table)
        table_dic = {}
        for table in tables:
        # Find all rows in the table
            
            rows = table.find_elements("xpath", tr_data)

            # Iterate through each row
            for row in rows:
                # Find th (header) and td (data) elements in the row
                headers = row.find_elements("xpath", th_data)
                data_cells = row.find_elements("xpath", td_data)

                # Extract text from th and td elements
                for header, data_cell in zip(headers, data_cells):
                    x = header.text
                    y = data_cell.text
                    table_dic[x] = y;
                    # print(f"x: {x}, y: {y}")
                # print(table_dic)clsc
        table_dic_cll.append(table_dic)
    table_json_data = json.dumps(table_dic_cll, ensure_ascii=False)
    print(table_json_data)
    # Don't forget to close the browser window when done
    driver.quit()
# """