from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import page_parser
from db import DB


print("Init DB")
db = DB("scrape.sqlite")

# Used only the first time to create tables
db.create()

# Test DB insert
db.insert(title="Ime strani", url="https://www.spletnastran.si")
db.insert(title="24 ur", url="https://www.24ur.com", parent_link=1)

print("\nStarting crawler")
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

browser.get('http://gov.si/')
urls, img_urls = page_parser.parse(browser)

print("URLs: %d, Image URLs: %d" % (len(urls), len(img_urls)))

browser.quit()
db.close()
