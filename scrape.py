from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.firefox.options import Options
import requests
import socket

import sys
import threading
import page_parser
from frontier import Frontier
from db.db import DB
import time


def crawler(crawler_id, database, front):
    print(f"\nStarting crawler {crawler_id}")
    options = Options()
    options.headless = True
    browser = Firefox(options=options)

    url = front.get_url()
    while url is not None:

        # Get and parse robots.txt
        robots_url = "http://" + url + "/robots.txt"
        res = requests.get(robots_url)

        if res.ok:
            disallowed_urls = page_parser.parse_robots(page_parser.get_domain(robots_url), res.text)
            front.add_disallowed_urls(disallowed_urls)

        # Get and parse
        if not front.allowed(url):
            url = front.get_url()
            continue

        page_url = "http://" + url

        # Check if 5 seconds passed since last request to this ip
        website_ip = socket.gethostbyname(page_parser.get_domain(page_url))
        if website_ip in front.request_history:
            diff = time.time() - front.request_history[website_ip]
            if diff < 5:
                # print("Waiting for " + page_url)
                front.add_url(url)
                url = front.get_url()
                continue
        front.request_history[website_ip] = time.time()

        # Finally get and parse page
        browser.get(page_url)

        title, urls, img_urls = page_parser.parse(browser)

        log_message = f"[{crawler_id}] Parsed {url}:" \
                      f"\n  --Title: {title}" \
                      f"\n  --urls found: {len(urls)}" \
                      f"\n  --images found: {len(img_urls)}"
        print(log_message)

        # TODO: Insert into database

        for new_url in urls:
            # Ignore non gov.si sites
            if page_parser.get_domain("http://" + new_url).endswith("gov.si"):
                front.add_url(new_url)

        url = front.get_url()

    browser.quit()


if __name__ == "__main__":
    db = DB(dbname="mydb")

    # Create tables from db/crawldb.sql
    db.create()

    # Test DB insert
    site_id = db.create_site(domain="24ur.com", robots_content="test robots content",
                             sitemap_content="some test sitemap content")
    db.create_page(site_id=site_id, page_type_code="HTML", url="24ur.com", html_content=None, http_status_code=200,
                   accessed_time=None)

    # Select all
    db.get_types()
    db.set_page_type(page_id=1, t="FRONTIER")

    starting_urls = ["gov.si", "evem.gov.si", "e-uprava.gov.si", "e-prostor.gov.si"]
    frontier = Frontier(starting_urls)

    # Number of workers can be passed as the parameter
    number_of_crawlers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Creating {number_of_crawlers} crawlers")
    for i in range(number_of_crawlers):
        # TODO make them use separate db connection or cursor, maybe that's threading problem
        thread = threading.Thread(target=crawler, args=(i, db, frontier))
        thread.start()

    # Drop all tables from the database
    # db.drop_all_tables()

    db.close()
