from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests
import re
from urllib.parse import urljoin
import time
import json
import math
import config

from models.site_structure import Data_structure, Site_structure, Table_data_structure

class Data:
    def __init__(self, images = None, map_link = None, table = None):
        self.images = images
        self.map_link = map_link
        self.table = table

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def scp_system(site_structure: Site_structure, get_type):
    # browser setting
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--headless")

    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome()

    #get parameters
    list_base_url = site_structure.list_base_url
    is_pagination = site_structure.is_pagination
    total_cnt_rex = site_structure.total_cnt_rex
    is_seperate = site_structure.is_seperate
    seperated_pages = site_structure.seperated_pages
    link_rex = site_structure.link_rex
    page_limit_exist = site_structure.page_limit_exist
    pg_param = site_structure.pg_param #pg_param
    limit_param = site_structure.limit_param #limi_param
    limit = site_structure.limit
    data_structure = site_structure.data_structure
    image_source_rex = data_structure.image_source_rex
    table_data_structure = data_structure.table_data_structure
    map_rex = data_structure.map_rex
    table_entire_rex = table_data_structure.table_entire_rex
    tr_rex = table_data_structure.tr_rex
    th_rex = table_data_structure.th_rex
    td_rex = table_data_structure.td_rex

    if list_base_url:
        driver.get(list_base_url)
        if total_cnt_rex is not None and total_cnt_rex != '':
            total_cnt_string = driver.find_element("xpath", total_cnt_rex).get_attribute('innerText').strip()
            number = re.search(r'\d+', str(total_cnt_string))
            if number:
                total_cnt = int(number.group())
            else:
                total_cnt = 0
            print("total_cnt:", total_cnt)
        # links = driver.find_elements('xpath',"")

    page_urls = []

    # if not page_limit_exist:
    page_limit_exist = [1, 1]

    if is_seperate:
        page_urls = seperated_pages
    else:
        if is_pagination and total_cnt_rex and limit:
            pages_count = math.floor(int(total_cnt) / limit) + 1;
            for i in range(1, pages_count + 1):
                page_url = list_base_url +  ( ("&" + f"{pg_param}={i}") if page_limit_exist[1] else "") + (("&" + f"{limit_param}={limit}") if page_limit_exist[0] else "")
                # if is_valid_url(page_url):
                page_urls.append(page_url)
        else:
            if is_valid_url(list_base_url):
                page_urls.append(list_base_url)
            if len(page_urls) == 0:
                page_urls.append(list_base_url)

    table_dic_cll = []
    all_data = []
    
    cnt = 0
    for page_url in page_urls:
        # if not is_valid_url(page_url):
        #     continue
        driver.get(page_url)
        driver.implicitly_wait(2)
        # getting the link elements
        links = driver.find_elements('xpath', link_rex)

        #getting the hrefs
        hrefs = []
        if len(links):
            t_name = links[0].tag_name
            if t_name == 'img':
                hrefs = [link.get_attribute("src") for link in links]
            elif t_name == 'a':
                hrefs = [link.get_attribute("href") for link in links]
                

        for item in hrefs:
            data = {}
            # Loop every item 
            driver.get(item)
            driver.implicitly_wait(2)
            
            images = []
            try:
                if image_source_rex:
                    image_elements = driver.find_elements('xpath', image_source_rex)
                    for image_element in image_elements:
                        if image_element.get_attribute('src'):
                            images.append(image_element.get_attribute('src'))
            except NoSuchElementException:
                print("No images found for this item.")
            map_link = None
            try:
                if map_rex:
                    map_element = driver.find_element('xpath', map_rex)
                    if map_element.tag_name == 'a':
                        map_link = map_element.get_attribute('href')
                    elif map_element.tag_name == 'iframe':
                        map_link = map_element.get_attribute('outerHTML')
            except NoSuchElementException:
                print("Map link not found for this item.")

            tables = []
            for table_entire_rex_item in table_entire_rex:
                one_table_group = driver.find_elements('xpath', table_entire_rex_item)

                for table in one_table_group:
                    tables.append(table)
            table_dic = {}
            for table in tables:
            # Find all rows in the table
                rows = table.find_elements("xpath", tr_rex)
                # Iterate through each row
                for row in rows:
                    # Find th (header) and td (data) elements in the row
                    headers = row.find_elements("xpath", th_rex)
                    data_cells = row.find_elements("xpath", td_rex)
                    # print(row.get_attribute('innerText').strip())
                    # Extract text from th and td elements
                    for header, data_cell in zip(headers, data_cells):
                        x = header.get_attribute('innerText').strip()
                        y = data_cell.get_attribute('innerText').strip()
                        if x and x != '' and y:
                            table_dic[x] = y;
                        # print(f"x: {x}, y: {y}")
                    # print(table_dic)clsc
            # table_dic_cll.append(table_dic)
            data = Data(images, map_link, table_dic)
            all_data.append(data)
            cnt = cnt + 1
            
            if (get_type == 'one') and cnt == 1:
                print(all_data)
                return all_data
            elif cnt == 2:
                return all_data
    # table_json_data = json.dumps(table_dic_cll, ensure_ascii=False)
    # print(table_json_data)
    driver.quit()
    return all_data
    # Don't forget to close the browser window when done
# """
