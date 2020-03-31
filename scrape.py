import hashlib
import os
from urllib.parse import urljoin

from seleniumrequests import Firefox
from selenium.webdriver.firefox.options import Options
import requests
import socket

import sys
import threading
import page_parser
from frontier import Frontier
from db.database import DB
import time
from logger import get_logger

PROJECT_ROOT = os.path.dirname(__file__)


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
        browser = Firefox(options=options, log_path=os.path.join(PROJECT_ROOT, 'logs/geckodriver.log'))

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

            # Fetch current page from the database FRONTIER
            page_id, page_type = db.get_page(url=url)
            if not page_id:
                # Maybe url came from the starting url seed, if so, we need to create page object
                if url in starting_urls:
                    # Create page object with FRONTIER type
                    page_id = db.create_page(
                        site_id=site_id,
                        url=url,
                        page_type_code="FRONTIER",
                    )
                else:
                    # Something went wrong in the process
                    self.logger.error(f"Page with url {url} is not in the database, but it should be as it was added to the frontier.")
                    url = front.get_url()
                    continue

            if not page_type or page_type != "FRONTIER":
                # I gues something went wrong, or some other crawler already finished this page (probably shouldn't have happened)
                self.logger.error(f"Page {page_id} with url {url} is of type {page_type} but it should be 'FRONTIER'.")
                url = front.get_url()
                continue

            # Everything is okay.
            # Finally get and parse page
            browser.get(url)

            # Set current time as the last request time for the current IP
            front.request_history[website_ip] = time.time()

            # if hash matches any, mark it as duplicate and skip it, also create link to which site it points
            html_content = browser.page_source
            html_content_hash = hashlib.sha1(html_content.encode('UTF-8')).hexdigest()
            duplicate_id, duplicate_site_id = self.db.get_page_by_hash(html_content_hash)
            if duplicate_id:
                db.set_page_type(
                    page_id=page_id,
                    page_type_code="DUPLICATE"
                )

                self.logger.info(f"Page {page_id} has a duplicate {duplicate_id} on url {url}.")
                db.create_link(page_id, duplicate_id)
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

                # Create page object with FRONTIER type
                page_id = db.create_page(
                    site_id=site_id,
                    url=new_url,
                    page_type_code="FRONTIER",
                )

            # Set current page as done, data type HTML
            db.set_page_type(page_id, "HTML")

            url = front.get_url()

        browser.quit()


if __name__ == "__main__":
    database = DB()

    starting_urls = ["https://www.gov.si", "http://evem.gov.si", "https://e-uprava.gov.si", "https://www.e-prostor.gov.si/"]

    # Check if url was already processed
    for url in starting_urls:
        page = database.get_page(url)
        if page:
            starting_urls.remove(url)

    # Fetch disallowed urls and pass it to the frontier as disallowed urls
    disallowed = database.get_disallowed_urls()

    # Get pages with type FRONTIER to fill the frontier
    frontier_pages = database.get_pages_by_type(page_type_code="FRONTIER")
    starting_urls.extend(frontier_pages)

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
