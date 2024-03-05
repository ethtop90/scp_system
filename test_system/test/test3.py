from selenium import webdriver
import re
from urllib.parse import urljoin
import time
import json
import math

url = "https://i-r-re.jimdofree.com/%EF%BC%91%EF%BD%8B-%EF%BC%91%EF%BD%8C%EF%BD%84%EF%BD%8B/"
driver = webdriver.Chrome()
driver.get(url)
para = "//a[text()='詳細' or .//text()='詳細']"
hrefs = driver.find_elements("xpath", para)
print(len(hrefs))

tables = []
texts = []
for href in hrefs:
    texts.append(href.get_attribute("href"))

for text in texts:

    driver.get(text)

    table_rex = "(//table[@class='mceEditable'])[position()<=2]"
    tables = driver.find_elements("xpath", table_rex)
    tr_rex = "//tr"
    th_rex = "(//td)[1]"
    td_rex = "(//td)[2]"
    for table in tables:
        trs = table.find_elements('xpath', tr_rex)
        for tr in trs:
            # print(tr.text)

            th = tr.find_element('xpath', th_rex)
            td = tr.find_element('xpath', td_rex)
            # print(th.text, ":", td.text)