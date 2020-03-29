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

        domain = page_parser.get_domain(url)
        base_url = page_parser.get_base_url(url)

        # Get and parse robots.txt
        robots_url = base_url + "robots.txt"
        res = requests.get(robots_url)

        if res.ok:
            disallowed_urls = page_parser.parse_robots(base_url, res.text)
            front.add_disallowed_urls(disallowed_urls)

        # Get and parse
        if not front.allowed(url):
            url = front.get_url()
            continue

        # Check if 5 seconds passed since last request to this ip
        website_ip = socket.gethostbyname(page_parser.get_domain(url))
        if website_ip in front.request_history:
            diff = time.time() - front.request_history[website_ip]
            # If it has been less than 5 seconds since last request, add url back to the frontier and get a new one
            if diff < 5:
                # print("Waiting for " + url)
                front.add_url(url)
                url = front.get_url()
                continue

        # Set current time as the last request time for the current IP
        front.request_history[website_ip] = time.time()

        # Finally get and parse page
        browser.get(url)

        title, urls, img_urls = page_parser.parse(browser)

        log_message = f"[{crawler_id}] Parsed {url}:" \
                      f"\n  --Title: {title}" \
                      f"\n  --urls found: {len(urls)}" \
                      f"\n  --images found: {len(img_urls)}"
        print(log_message)

        # Check if site with current domain already exists, if not create site
        site_id = db.get_site(domain=domain)
        if not site_id:
            site_id = db.create_site(domain=domain, robots_content=None, sitemap_content=None)

        # Check if page with current url already exists, if not create page
        page_id = db.get_page(url=url)
        if not page_id:
            # TODO check & compare page content_hash
            # Also check if page content_hash matches
            # duplicate = db.check_page_content_hash(...)

            page_type = "HTML"
            # if duplicate:
            #     page_type = "DUPLICATE

            # No duplicate was found, create page
            # TODO what about http_status
            # db.create_page(site_id=site_id, page_type_code=page_type, url=url, html_content=None, http_status_code=200)

        for new_url in urls:
            # Ignore non gov.si sites
            if page_parser.get_domain(new_url).endswith("gov.si"):
                front.add_url(new_url)

        url = front.get_url()

    browser.quit()


if __name__ == "__main__":
    db = DB()

    # Create tables from db/crawldb.sql
    db.create()

    # Test DB insert
    # site_id = db.create_site(domain="24ur.com", robots_content="test robots content",
    #                          sitemap_content="some test sitemap content")
    # db.create_page(site_id=site_id, page_type_code="HTML", url="24ur.com", html_content=None, http_status_code=200,
    #                accessed_time=None)

    # Select all
    # db.get_types()
    # db.set_page_type(page_id=1, t="FRONTIER")

    # First we insert those 4 sites to the database
    starting_urls = ["https://www.gov.si", "http://evem.gov.si", "https://e-uprava.gov.si", "https://www.e-prostor.gov.si/"]
    frontier = Frontier(starting_urls)

    # Number of workers can be passed as the parameter
    number_of_crawlers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Creating {number_of_crawlers} crawlers")
    for i in range(number_of_crawlers):
        # TODO make them use separate db connection or cursor, maybe that's threading problem (see postgres connection pool)
        thread = threading.Thread(target=crawler, args=(i, db, frontier))
        thread.start()

    # Drop all tables from the database
    # db.drop_all_tables()

    db.close()
