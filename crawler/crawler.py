import hashlib
from urllib.parse import urljoin

from seleniumrequests import Firefox
from selenium.webdriver.firefox.options import Options
import socket

import threading
import urllib.robotparser
from crawler import page_parser
from db.database import DB
import time
from datetime import datetime
from logger import get_logger


class Crawler:
    thread = None

    def __init__(self, name=None, front=None, log_level=None, log_path=None):
        self.name = name
        self.front = front
        self.db = None
        self.thread = None

        # Start logger
        self.logger = get_logger(name=name, level=log_level, log_path=log_path)

    def start(self):
        # Save thread to the instance and start crawling
        if not self.thread or not self.thread.is_alive():
            # Create new database connection
            self.db = DB(logger=self.logger)

            self.thread = threading.Thread(target=self.crawl)
            self.thread.start()
            return self.thread
        else:
            self.logger.error("Can't start a new thread, thread is already running.")
            return None

    def stop(self):
        if self.db:
            self.db.close()

    def create_site(self, base_url, domain):
        db = self.db
        add_robots_parser = True
        robots_content = None
        site_maps = None

        # Site doesn't exists, we can safely fetch robots.txt file without checking any time limit
        # Get and parse robots.txt
        if not base_url:
            self.logger.error(f"No base url for {domain}")
        if not domain:
            print(f"no domain for {base_url}")

        robots_url = urljoin(base_url, "robots.txt")
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            if rp.default_entry:
                robots_content = str(rp.default_entry)

            # TODO make use of site maps
            if rp.site_maps():
                site_maps = "\n".join(rp.site_maps())

        except Exception as e:
            self.logger.warning(e)
            add_robots_parser = False

        site_id = db.create_site(domain=domain, robots_content=robots_content, sitemap_content=site_maps)

        # Add robotsparser to the frontier's site robot parsers
        if add_robots_parser:
            self.front.add_site_robots(site_id=site_id, rp=rp)

        return site_id

    def crawl(self):
        db = self.db
        front = self.front
        self.logger.info(f"Starting crawler {self.name}")

        options = Options()
        options.headless = True
        browser = Firefox(options=options, service_log_path='logs/geckodriver.log')

        # Wait 5 seconds before throwing exception when not finding elements
        browser.implicitly_wait(5)

        url = front.get_url()
        while url is not None:
            self.logger.info(f"Check url {url}")

            domain = page_parser.get_domain(url)
            base_url = page_parser.get_base_url(url)

            # Check if site with current domain already exists, if not create new site
            site_id, robots_content = db.get_site(domain=domain)
            if not site_id:
                # Site doesn't exists, create it
                site_id = self.create_site(base_url, domain)

            # Check if url is allowed (it is not inside frontier's disallowed urls)
            if not front.can_fetch(site_id, url):
                self.logger.info(f"Skip not allowed URL: {url}")
                # page_type = "DISALLOWED"
                url = front.get_url()
                continue

            # Fetch current page from the database FRONTIER
            if url.find("eprostor.si") >= 0:
                print(url)

            page_id, page_type = db.get_page(url=url)
            if not page_id:
                # Maybe url came from the starting url seed, if so, we need to create page object
                if url in front.starting_urls:
                    page_type = "FRONTIER"

                    # Create canonical version of the url
                    url = page_parser.canonicalize(base_url, url)

                    # Create page object with FRONTIER type
                    page_id = db.create_page(
                        site_id=site_id,
                        url=url,
                        page_type_code=page_type,
                    )
                else:
                    # Something went wrong in the process
                    self.logger.error(f"Page with url {url} is not in the database, but it should be as it was added to the frontier.")
                    url = front.get_url()
                    continue

            if page_type != "FRONTIER":
                # I gues something went wrong, or some other crawler already finished this page (probably shouldn't have happened)
                self.logger.error(f"Page {page_id} with url {url} is of type {page_type} but it should be 'FRONTIER'.")
                # TODO no! should add page as duplicate
                url = front.get_url()
                continue

            # Check if 5 seconds have passed since the last request to this IP
            try:
                website_ip = socket.gethostbyname(domain)
            except Exception as e:
                db.set_page_type(page_id, "DOMAIN_ERROR")
                self.logger.warning(f"Can't resolve domain name {domain}. Skip page {page_id} and set it as DOMAIN_ERROR.")
                url = front.get_url()
                continue

            if website_ip in front.request_history:
                diff = time.time() - front.request_history[website_ip]

                # If it has been less than 5 seconds since last request, add url back to the frontier and get a new one
                if diff < 5:
                    # print("Waiting for " + url)
                    front.add_url(url)
                    url = front.get_url()
                    continue

            # TODO first do HEAD request to get page headers, maybe see if url is file etc...

            # TODO make some minimal delay (1 sec then GET actual content)

            # Everything is okay.
            # Finally get and parse page
            accessed_time = datetime.now()
            try:
                browser.get(url)
            except Exception as e:
                self.logger.error(f"Webdriver exception occured while fetching {url}. {e}")
                db.set_page_type(page_id, "WEBDRIVER_ERROR")
                # TODO set page accessed time
                url = front.get_url()
                continue

            # Set current time as the last request time for the current IP
            front.request_history[website_ip] = time.time()

            # if hash matches any, mark it as duplicate and skip it, also create link to which site it points
            html_content = browser.page_source
            html_content_hash = hashlib.sha1(html_content.encode('UTF-8')).hexdigest()
            duplicate_id, duplicate_site_id = self.db.get_page_by_hash(html_content_hash)
            if duplicate_id:
                db.update_page(
                    page_id=page_id,
                    fields=dict(
                        page_type_code="DUPLICATE",
                        accessed_time=accessed_time
                    )
                )

                self.logger.info(f"Page {page_id} has a duplicate {duplicate_id} on url {url}.")
                db.create_link(page_id, duplicate_id)
                url = front.get_url()
                continue

            # TODO set page_type appropriately, not just HTML
            page_id = db.update_page(
                page_id=page_id,
                fields=dict(
                    page_type_code="HTML",
                    html_content=html_content,
                    html_content_hash=html_content_hash,
                    http_status_code=200,
                    accessed_time=accessed_time
                )
            )

            title, urls, img_urls = page_parser.parse(browser)

            self.logger.info(
                f"Parsed {url}:" 
                f"\n  --Title: {title.encode('UTF-8')}"
                f"\n  --urls found: {len(urls)}"
                f"\n  --images found: {len(img_urls)}"
            )

            for new_url in urls:
                if new_url.find("eprostor.si") >= 0:
                    print(url)

                # Create canonical version of the url
                new_url = page_parser.canonicalize(base_url, new_url)

                new_url_domain = page_parser.get_domain(new_url)

                # Ignore non gov.si sites
                if not new_url_domain.endswith("gov.si"):
                    continue

                existing_site_id = site_id

                # Check if domain matches current site_id
                if new_url_domain == domain:
                    if not front.can_fetch(existing_site_id, new_url):
                        continue
                else:
                    # if not try to fetch site with this domain from the database, if it exists,
                    # it means it already has robots.txt processed so we can check if we it is allowed to be added to the frontier or not
                    existing_site_id, _ = db.get_site(new_url_domain)

                # If site doesn't exist, create new one
                if not existing_site_id:
                    new_base_url = page_parser.get_base_url(new_url)
                    existing_site_id = self.create_site(new_base_url, new_url_domain)

                # Check if page with current url already exists, if not add url to frontier
                duplicate_page_id, new_page_type = db.get_page(url=new_url)
                if duplicate_page_id:
                    new_page_id = db.create_page(
                        site_id=existing_site_id,
                        url=new_url,
                        page_type_code="DUPLICATE"
                    )

                    # Create a link
                    db.create_link(new_page_id, duplicate_page_id)
                    continue

                if new_url == "https://e-uprava.gov.si/":
                    print(new_url)

                # Everything was good, we can add this url to the frontier.
                front.add_url(new_url)

                # Create page object with FRONTIER type
                db.create_page(
                    site_id=existing_site_id,
                    url=new_url,
                    page_type_code="FRONTIER",
                )

            for img_url in img_urls:
                if img_url.startswith("/"):
                    # Relative url
                    img_url = urljoin(base_url, img_url)
                if not img_url.startswith("http"):
                    # Url not valid
                    continue
                img_type = img_url.split("/")[-1]
                if "." in img_type:
                    img_type = img_type.split(".")[-1]
                else:
                    img_type = "/"
                img_type = img_type.lower()
                db.create_image(page_id, img_url, img_type, datetime.now())

            url = front.get_url()

        browser.quit()
