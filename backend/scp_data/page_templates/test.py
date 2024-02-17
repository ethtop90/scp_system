# 1 site

from selenium import webdriver

# Assuming you have already initialized the webdriver (e.g., ChromeDriver)
driver = webdriver.Chrome()
driver.get("https://earth-fudosan.com/59896/")

# Find links with "background-image" style
links_with_background_image = driver.find_elements_by_xpath('//a[contains(@style, "background-image")]')

# Print the href attribute of each link
for link in links_with_background_image:
    print(link.get_attribute("href"))

# Don't forget to close the browser window when done
driver.quit()
