from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import sys
import threading
import page_parser
from frontier import Frontier
from db import DB


def crawler(crawler_id, database, front):
    print(f"\nStarting crawler {crawler_id}")
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    url = front.get_url()
    while url is not None:
        browser.get("http://" + url)

        # Parse page
        title, urls, img_urls = page_parser.parse(browser)

        log_message = f"[{crawler_id}] Parsed {url}:" \
                      f"\n  --Title: {title}" \
                      f"\n  --urls found: {len(urls)}" \
                      f"\n  --images found: {len(img_urls)}"
        print(log_message)

        # Insert into database
        # db.insert(title=title, url=url)

        for new_url in urls:
            frontier.add_url(new_url)
        url = front.get_url()

    browser.quit()


if __name__ == "__main__":
    print("Init DB")
    db = DB("scrape.sqlite")

    # Used only the first time to create tables
    db.create()
    # Test DB insert
    # db.insert(title="Ime strani", url="https://www.spletnastran.si")
    # db.insert(title="24 ur", url="https://www.24ur.com", parent_link=1)
    db.test()

    starting_urls = ["gov.si", "evem.gov.si", "e-uprava.gov.si", "e-prostor.gov.si"]
    frontier = Frontier(starting_urls)

    number_of_crawlers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"Creating {number_of_crawlers} crawlers")
    for i in range(number_of_crawlers):
        thread = threading.Thread(target=crawler, args=(i, db, frontier))
        thread.start()
    db.close()
