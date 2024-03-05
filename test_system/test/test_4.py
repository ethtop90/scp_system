from selenium import webdriver
import re
from urllib.parse import urljoin
import time
import json
import math


url = "https://www.clean-estate.com/?bukken=a&shu=&mid=999&nor=999&so=kak&ord=&s="
driver = webdriver.Chrome()
driver.get(url)

hrefs = driver.find_elements('xpath', "//a[div[@class='list_details_button']]")

for href in hrefs:
    print(href.get_attribute('href'))

# link_rex = "//div[@class='main_estList']//li//a"
# link_elements = driver.find_elements('xpath', link_rex)
# for link in link_elements:
#     print(link.get_attribute('href'))  