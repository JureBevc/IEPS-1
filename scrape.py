import sys
import urllib.robotparser

from crawler.crawler import Crawler
from crawler.frontier import Frontier
from db.database import DB
from logger import get_logger

logger = get_logger(name="scrape", level="INFO", log_path="logs/scrape.log")


def main():
    db = DB(logger=logger)

    # Get every site's robots.txt and parse it and store it to site_robots dictionary in the frontier
    site_robots = dict()

    for site in db.get_all_sites(has_robots=True):
        robots_content = site[1]
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(robots_content.split("\n"))
        site_robots[site[0]] = rp

    starting_urls = ["https://www.gov.si/", "http://evem.gov.si/", "https://e-uprava.gov.si/", "https://www.e-prostor.gov.si/"]

    # Check if url was already processed
    for url in starting_urls.copy():
        page, page_type = db.get_page(url)
        if page:
            starting_urls.remove(url)

    # Get pages with type FRONTIER to fill the frontier
    frontier_pages = db.get_pages_by_type(page_type_code="FRONTIER")
    starting_urls.extend([p[0] for p in frontier_pages])

    db.close()

    frontier = Frontier(starting_urls, site_robots)

    # Number of workers can be passed as the parameter
    number_of_crawlers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    logger.info(f"Creating {number_of_crawlers} crawlers")
    crawlers = dict()

    for i in range(number_of_crawlers):
        crawler = Crawler(name=f"crawler_{i}", front=frontier, log_level="ERROR", log_path="logs/crawldb.log")
        crawlers[i] = crawler
        crawler.start()


if __name__ == "__main__":
    main()
