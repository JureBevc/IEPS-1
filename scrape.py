import hashlib
from urllib.parse import urljoin

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
from logger import get_logger


class Crawler:
    thread = None

    def __init__(self, name=None, front=None):
        self.name = name
        self.front = front
        self.db = None
        self.thread = None

        # Start logger
        self.logger = get_logger(name)

    def start(self):
        # Save thread to the instance and start crawling
        if not self.thread or not self.thread.is_alive():
            # Create new database connection
            # TODO also (see postgres connection pool)
            self.db = DB(logger=self.logger)

            self.thread = threading.Thread(target=self.crawl)
            self.thread.start()
        else:
            self.logger.error("Can't start a new thread, thread is already running.")

    def stop(self):
        if self.db:
            self.db.close()

    def crawl(self):
        db = self.db
        front = self.front
        self.logger.info(f"Starting crawler {self.name}")

        options = Options()
        options.headless = True
        browser = Firefox(options=options)

        url = front.get_url()
        while url is not None:
            self.logger.info(f"Check url {url}")

            domain = page_parser.get_domain(url)
            base_url = page_parser.get_base_url(url)

            # Check if site with current domain already exists, if not create new site
            site_id, robots_content = db.get_site(domain=domain)
            if not site_id:
                # Site doesn't exists, we can safely fetch robots.txt file without checking any time limit
                # Get and parse robots.txt
                robots_url = urljoin(base_url, "robots.txt")
                res = requests.get(robots_url)

                if res.ok and res.text:
                    robots_content = res.text

                # TODO also fetch sitemap
                site_id = db.create_site(domain=domain, robots_content=robots_content, sitemap_content=None)

                disallowed_urls = page_parser.parse_robots(base_url, robots_content)

                # Add new disallowed urls to the frontier's disallowed urls
                front.add_disallowed_urls(disallowed_urls)

                # Add new disallowed urls to the database
                db.create_disallowed_urls(site_id, disallowed_urls)

            # Check if url is allowed (is not inside disallowed urls)
            if not front.allowed(url):
                url = front.get_url()
                continue

            # Check if 5 seconds passed since last request to this IP
            website_ip = socket.gethostbyname(domain)
            if website_ip in front.request_history:
                diff = time.time() - front.request_history[website_ip]

                # If it has been less than 5 seconds since last request, add url back to the frontier and get a new one
                if diff < 5:
                    # print("Waiting for " + url)
                    front.add_url(url)
                    url = front.get_url()
                    continue

            # Everything is okay, we can fetch page.
            # Finally get and parse page
            browser.get(url)

            # Set current time as the last request time for the current IP
            front.request_history[website_ip] = time.time()

            # if hash matches any, mark it as duplicate and skip it, also create link to which site it points
            html_content = browser.page_source
            html_content_hash = hashlib.sha1(html_content.encode('UTF-8')).hexdigest()
            duplicate_id, duplicate_site_id = self.db.get_page_by_hash(html_content_hash)
            if duplicate_id:
                page_id = db.create_page(
                    site_id=duplicate_site_id,
                    page_type_code="DUPLICATE",
                    url=url,
                    http_status_code=200
                )

                self.logger.info(f"Page {duplicate_id} duplicate was found on url {url}.")
                db.create_link(duplicate_id, page_id)
                url = front.get_url()
                continue

            # TODO set page_type appropriately, not just HTML
            page_id = db.create_page(
                site_id=site_id,
                page_type_code="HTML",
                url=url,
                html_content=html_content,
                html_content_hash=html_content_hash,
                http_status_code=200
            )
            self.logger.info(f"New page was created {page_id} with url {url}.")

            title, urls, img_urls = page_parser.parse(browser)

            log_message = f"[{self.name}] Parsed {url}:" \
                          f"\n  --Title: {title}" \
                          f"\n  --urls found: {len(urls)}" \
                          f"\n  --images found: {len(img_urls)}"

            self.logger.info(log_message)

            for new_url in urls:
                # Create canonical version of the url
                new_url = page_parser.canonicalize(base_url, new_url)

                new_url_domain = page_parser.get_domain(new_url)

                # new_base_url = page_parser.get_base_url(new_url)

                # Ignore non gov.si sites
                if not new_url_domain.endswith("gov.si"):
                    continue

                # Url was found in some site's robots.txt file, ignore it
                if not front.allowed(new_url):
                    continue

                # # Check if site with current domain already exists, if not create new site
                # site_id, robots_content = db.get_site(domain=new_url_domain)
                # if not site_id:
                #     # Site doesn't exists, we can safely fetch robots.txt file without checking any time limit
                #     # Get and parse robots.txt
                #     robots_url = urljoin(new_base_url, "robots.txt")
                #     res = requests.get(robots_url)
                #
                #     if res.ok and res.text:
                #         robots_content = res.text
                #
                #     # TODO also fetch sitemap
                #     site_id = db.create_site(domain=new_url_domain, robots_content=robots_content, sitemap_content=None)
                #
                #     disallowed_urls = page_parser.parse_robots(new_base_url, robots_content)
                #
                #     # Add new disallowed urls to the frontier's disallowed urls
                #     front.add_disallowed_urls(disallowed_urls)
                #
                #     # Add new disallowed urls to the database
                #     db.create_disallowed_urls(site_id, disallowed_urls)

                # Check if page with current url already exists, if not add url to frontier
                duplicate_page_id = db.get_page(url=new_url)
                if duplicate_page_id:
                    # TODO what about http_status
                    db.create_page(
                        site_id=duplicate_site_id,
                        page_type_code="DUPLICATE",
                        http_status_code=200
                    )
                    continue

                # Everything was good, we can add this url to the frontier.
                front.add_url(new_url)

            # Set current page as done, data type HTML
            db.set_page_type(page_id, "HTML")

            url = front.get_url()

        browser.quit()


if __name__ == "__main__":
    database = DB()

    # Create tables from db/crawldb.sql
    database.create()
    # TODO wait until db is created, takes 5 secs

    # Test DB insert
    # site_id = database.create_site(domain="24ur.com", robots_content="test robots content",
    #                          sitemap_content="some test sitemap content")
    # database.create_page(site_id=site_id, page_type_code="HTML", url="24ur.com", html_content=None, http_status_code=200,
    #                accessed_time=None)

    # Select all
    # database.get_types()
    # database.set_page_type(page_id=1, t="FRONTIER")

    # First we insert those 4 sites to the database
    starting_urls = ["https://www.gov.si", "http://evem.gov.si", "https://e-uprava.gov.si", "https://www.e-prostor.gov.si/"]

    # Fetch disallowed urls and pass it to the frontier as disallowed urls
    disallowed = database.get_disallowed_urls()

    # Drop all tables from the database
    # database.drop_all_tables()
    database.close()

    frontier = Frontier(starting_urls, disallowed)

    # Number of workers can be passed as the parameter
    number_of_crawlers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Creating {number_of_crawlers} crawlers")
    crawlers = dict()

    for i in range(number_of_crawlers):
        crawler = Crawler(name=f"crawler_{i}", front=frontier)
        crawlers[i] = crawler
        crawler.start()
