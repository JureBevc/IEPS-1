from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import page_parser

print("Starting crawler")

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

browser.get('http://gov.si/')
urls, img_urls = page_parser.parse(browser)

print("URLs: %d, Image URLs: %d" % (len(urls), len(img_urls)))

browser.quit()
