from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import urltools
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def canonicalize(base_url, url):
    """
        https://github.com/rbaier/python-urltools
    """

    # TODO "https://e-uprava.gov.si/*/" does not get parsed correctly
    # Fix relative urls
    url = urljoin(base_url, url)

    # lowercasing the scheme and hostname
    # convert hostname to IDN format
    # taking out default port if present :80
    # collapsing the path (./, ../, etc)
    # removing the last character in the hostname if it is ‘.’
    # unquoting any % escaped characters (where possible)
    # sort query parameters
    try:
        url = urltools.normalize(url)
    except Exception as e:
        print(e)

    # Remove url fragments
    url = urldefrag(url).url

    # TODO Add a trailing slash? Maybe this si not okay in every case?
    if not url.endswith("/"):
        parameters = urltools.parse(url).query
        # Don't add trailing slash if url has parameters
        # if not parameters:
        #     url += "/"

    return url


def get_domain(url):
    parsed_uri = urltools.split(url)
    return parsed_uri.netloc


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def parse_robots(base_url, robots_txt):
    disallowed_urls = []

    all_agents = False
    user_agent = "User-agent:"
    disallow = "Disallow:"
    for line in robots_txt.split("\n"):
        if line.startswith(user_agent):
            if line.split(user_agent)[1].strip() == "*":
                all_agents = True
            else:
                all_agents = False
        elif all_agents and line.startswith(disallow):
            disallowed_url = line.split(disallow)[1].strip()
            disallowed_url = canonicalize(base_url, disallowed_url)
            disallowed_urls.append(disallowed_url)

    return disallowed_urls


def parse(browser):
    urls = []
    img_urls = []
    title = browser.title
    email_regex = """(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    html = browser.page_source

    # Only need to check if onclick attr has: href= or location=
    # Create beautiful soup instance to find onclick links
    soup = BeautifulSoup(html, 'html.parser')
    for onclick in soup.body.find_all(attrs={'onclick': True}):
        ref = onclick.attrs.get('onclick').strip()
        found = ref.find("href=")
        if found >= 0:
            url = ref[found+5:].strip().strip("\'").strip().strip("\"").strip()
            if not re.search(email_regex, url):
                urls.append(url)
            continue

        found = ref.find("location=")
        if found >= 0:
            url = ref[found+9:].strip().strip("\'").strip().strip("\"").strip()
            if not re.search(email_regex, url):
                urls.append(url)
            continue

    # try:
    # links = browser.find_elements_by_tag_name("a").copy()
    # for link in links:
    # Wait 4 seconds before throwing StaleElementReferenceException
    try:
        links = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        for link in links:
            ref = link.get_attribute("href")
            if ref:
                ref = ref.strip()
                if not re.search(email_regex, ref):
                    urls.append(ref)

    except Exception as e:
        print(e)

    # except Exception as e:
    #     print(e)

    try:
        # images = browser.find_elements_by_tag_name("img").copy()
        images = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        for image in images:
            src = image.get_attribute("src")
            if src:
                img_urls.append(src)
    except Exception as e:
        print(e)

    return title, urls, img_urls
