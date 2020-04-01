from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import urltools


def canonicalize(base_url, url):
    """
        this is a canonical() copy, just for the reference, so I (Luka) don't delete your code.
        Inspiration taken from:
            https://stackoverflow.com/questions/10584861/canonicalize-normalize-a-url

        Good library:
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

    # Add a trailing slash? Maybe this si not okay in every case? for example images
    if not url.endswith("/"):
        parameters = urltools.parse(url).query
        # Don't add trailing slash if url has parameters
        if not parameters:
            url += "/"

    return url


def get_domain(url):
    parsed_uri = urltools.split(url)
    return parsed_uri.netloc


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def parse_robots(base_url, robots_txt):
    disallowed_urls = []
    site_map_urls = []

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

    html = browser.page_source

    # Create beautiful soup instance to find onclick links
    soup = BeautifulSoup(html, 'html.parser')
    for onclick in soup.body.find_all(attrs={'onclick': True}):
        ref = onclick.attrs.get('onclick').strip()
        found = ref.find("href=")
        if found >= 0:
            url = ref[found+5:].strip().strip("\'").strip().strip("\"").strip()
            urls.append(url)
            continue

        found = ref.find("location=")
        if found >= 0:
            url = ref[found+9:].strip().strip("\'").strip().strip("\"").strip()
            urls.append(url)
            continue

    # Only need to check if onClick tag has: location.href or document.location
    links = browser.find_elements_by_tag_name("a")
    for link in links:
        ref = link.get_attribute("href")
        if ref:
            urls.append(ref)
    images = browser.find_elements_by_tag_name("img")
    for image in images:
        src = image.get_attribute("src")
        if src:
            img_urls.append(src)
    return title, urls, img_urls
