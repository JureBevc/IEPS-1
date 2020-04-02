import hashlib
from urllib.parse import urljoin

import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxProfile
from seleniumrequests import Firefox
from selenium.webdriver.firefox.options import Options
import socket

import threading
import urllib.robotparser
from crawler import page_parser
import psycopg2
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
        self.stop_signal = False

        self.request_headers = requests.utils.default_headers()
        self.request_headers.update(
            {"User-Agent": "fri-ieps-crawler-lj"}
        )

        self.common_content_types = {
            'application/vnd.ms-powerpoint': 'PPT',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'PPTX',
            'application/msword': 'DOC',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
            'application/pdf': 'PDF',
        }

        # Start logger
        self.logger = get_logger(name=name, level=log_level, log_path=log_path)

    def start(self):
        # Save thread to the instance and start crawling
        if not self.thread or not self.thread.is_alive():
            # Create new database connection
            self.db = DB(logger=self.logger)

            self.thread = threading.Thread(target=self.crawl)
            self.thread.setDaemon(True)
            self.thread.start()
            return self.thread
        else:
            self.logger.error("Can't start a new thread, thread is already running.")
            return None

    def stop(self):
        self.stop_signal = True

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
            self.logger.error(f"no domain for {base_url}")

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

        try:
            site_id = db.create_site(domain=domain, robots_content=robots_content, sitemap_content=site_maps)

            # Add robotsparser to the frontier's site robot parsers
            if add_robots_parser:
                self.front.add_site_robots(site_id=site_id, rp=rp)
        except psycopg2.IntegrityError:
            site_id, _ = db.get_site(domain=domain)
            print("Unique domain error")

        return site_id

    def crawl(self):
        db = self.db
        front = self.front
        self.logger.info(f"Starting crawler {self.name}")

        options = Options()
        options.headless = True

        # Set user agent as IEPS
        ieps_profile = FirefoxProfile()
        ieps_profile.set_preference("general.useragent.override", "fri-ieps-crawler-lj")
        options.set_capability('unhandledPromptBehavior', 'dismiss')

        browser = Firefox(firefox_profile=ieps_profile, options=options, service_log_path='logs/geckodriver.log')

        # Timeout before site is marked as TIMEOUT
        browser.set_page_load_timeout(20)

        # Wait 5 seconds before throwing exception when not finding elements
        browser.implicitly_wait(8)

        url = front.get_url()
        while url is not None:
            if self.stop_signal:
                break
            self.logger.info(f"Check url {url}")

            # Fetch current page from the database FRONTIER
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

            page_id, page_type = db.get_page(url=url)
            if not page_id:
                # Maybe url came from the starting url seed, if so, we need to create page object
                if url in front.starting_urls:
                    page_type = "FRONTIER"

                    # Create canonical version of the url
                    url = page_parser.canonicalize(base_url, url)

                    try:
                        # Create page object with FRONTIER type
                        page_id = db.create_page(
                            site_id=site_id,
                            url=url,
                            page_type_code=page_type,
                        )
                    except psycopg2.IntegrityError:
                        # Another thread has already created this page, so we can skip it here.
                        continue
                else:
                    # Something went wrong in the process
                    self.logger.error(f"Page with url {url} is not in the database, but it should be as it was added to the frontier.")
                    url = front.get_url()
                    continue

            if page_type != "FRONTIER":
                if url not in front.starting_urls:
                    self.logger.error(f"Page {page_id} with url {url} is of type {page_type} but it should be 'FRONTIER'.")
                    # TODO should add page as duplicate? this shouldn't happen
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
                    front.add_url(url)
                    url = front.get_url()
                    continue

            redirected = None
            response_status = 200
            try:
                response = requests.head(url, headers=self.request_headers)
                response_status = response.status_code
                if 300 <= response_status < 400:
                    redirected = response_status

                headers = response.headers
                content_type = headers.get('content-type')
                content_length = headers.get('content-length')
                location = headers.get('location')

                # Check for redirects and follow them untill you get to the final resource
                while location:
                    self.logger.info(f"Follow redirect on: {location}")
                    redirect = requests.head(location, headers=self.request_headers)
                    response_status = redirect.status_code
                    headers = redirect.headers
                    location = headers.get('location')
                    content_type = headers.get('content-type')
                    content_length = headers.get('content-length')

                if content_type:
                    content_type = content_type.lower()
                    if content_type.find('text/html') < 0:
                        self.logger.info(f"Found BINARY with content-type: {content_type} on {url}")
                        db.update_page(
                            page_id=page_id,
                            fields=dict(
                                page_type_code="BINARY",
                                http_status_code=response_status if response_status else redirected,
                                accessed_time=datetime.now()
                            )
                        )

                        common_type = self.common_content_types.get(content_type)
                        db.create_page_data(page_id=page_id, data_type_code=common_type, data=content_type)

                        url = front.get_url()
                        continue
                else:
                    # Content is bigger than 10MB
                    # 15 == 15728640
                    # TODO should do something, set this page as BINARY and skip it, because it is too big?
                    if content_length and int(content_length) > 10485760:
                        self.logger.warning(f"Content bigger than 10MB do something. {url}")

                self.logger.debug(headers)
            except Exception as e:
                self.logger.info(f"HEAD method is not possible on {url}. {e}")

            # Wait 1 second before doing another GET request
            time.sleep(1)

            # Everything is okay.
            # Finally get and parse page
            accessed_time = datetime.now()
            try:
                browser.get(url)
            except TimeoutException:
                db.update_page(
                    page_id=page_id,
                    fields=dict(
                        page_type_code="TIMEOUT",
                        accessed_time=accessed_time
                    )
                )
                url = front.get_url()
                continue
            except Exception as e:
                db.update_page(
                    page_id=page_id,
                    fields=dict(
                        page_type_code="WEBDRIVER_ERROR",
                        accessed_time=accessed_time,
                        http_status_code=response_status if response_status else redirected
                    )
                )
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

                self.logger.info(f"Page {page_id} is a duplicate {duplicate_id} on url {url}.")
                db.create_link(page_id, duplicate_id)
                url = front.get_url()
                continue

            db.update_page(
                page_id=page_id,
                fields=dict(
                    page_type_code="HTML",
                    html_content=html_content,
                    html_content_hash=html_content_hash,
                    http_status_code=response_status if response_status else redirected,
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
                # Create canonical version of the url
                new_url = page_parser.canonicalize(base_url, new_url)

                new_url_domain = page_parser.get_domain(new_url)

                # Ignore non gov.si sites
                if not new_url_domain.endswith("gov.si"):
                    continue

                existing_site_id = site_id

                # Check if domain matches current site_id
                if new_url_domain != domain:
                    # if not try to fetch site with this domain from the database, if it exists,
                    # it means it already has robots.txt processed so we can check if we it is allowed to be added to the frontier or not
                    existing_site_id, _ = db.get_site(new_url_domain)

                if existing_site_id:
                    if not front.can_fetch(existing_site_id, new_url):
                        continue
                else:
                    # If site doesn't exist, create new one
                    new_base_url = page_parser.get_base_url(new_url)
                    existing_site_id = self.create_site(new_base_url, new_url_domain)

                # Check if page with current url already exists, if not add url to frontier
                duplicate_page_id, duplicate_page_type = db.get_page(url=new_url)
                if duplicate_page_id:
                    try:
                        new_page_id = db.create_page(
                            site_id=existing_site_id,
                            url=new_url,
                            page_type_code="DUPLICATE"
                        )

                        # Create a link
                        db.create_link(new_page_id, duplicate_page_id)
                    except psycopg2.IntegrityError:
                        # Another thread has already created this page, so we can skip it here.
                        pass

                    continue

                # Everything was good, we can add this url to the frontier.
                front.add_url(new_url)

                # Create page object with FRONTIER type
                try:
                    db.create_page(
                        site_id=existing_site_id,
                        url=new_url,
                        page_type_code="FRONTIER",
                    )
                except psycopg2.IntegrityError:
                    # Another thread has already created this page, so we can skip it here.
                    continue

            for img_url in img_urls:
                # Relative url
                if img_url.startswith("/"):
                    img_url = urljoin(base_url, img_url)

                # Check if base64 or something else
                if not img_url.startswith("http"):
                    # Url not valid
                    continue
                filename = img_url.split("/")[-1]
                if len(filename) <= 255:
                    if "." in filename:
                        img_type = filename.split(".")[-1]
                    else:
                        img_type = "/"

                    if len(img_type) > 50:
                        continue

                    img_type = img_type.lower()
                    db.create_image(page_id, filename, img_type, datetime.now())

            url = front.get_url()

        browser.quit()
        if self.db:
            self.db.close()
