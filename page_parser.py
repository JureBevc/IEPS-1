from url_normalize import url_normalize
from urllib.parse import urlparse, urljoin
import urltools


def canonicalize(base_url, url):
    """
        this is a canonical() copy, just for the reference, so I (Luka) don't delete your code.
        Inspiration taken from:
            https://stackoverflow.com/questions/10584861/canonicalize-normalize-a-url

        Good library:
            https://github.com/rbaier/python-urltools
    """
    # Fix relative urls
    url = urljoin(base_url, url)

    # lowercasing the scheme and hostname
    # convert hostname to IDN format
    # taking out default port if present :80
    # collapsing the path (./, ../, etc)
    # removing the last character in the hostname if it is ‘.’
    # unquoting any % escaped characters (where possible)
    # sort query parameters
    url = urltools.normalize(url)

    # TODO add trailing slash?

    return url


def canonical(url):
    url = url.split("?")[0]
    url = url.split("#")[0]
    url = url_normalize(url)

    # TODO also check if url is relative example: '/assets/img/test.jpg' ?

    if url.startswith("http://"):
        url = url[7:]
    if url.startswith("https://"):
        url = url[8:]
    if url.startswith("www."):
        url = url[4:]
    if url.endswith("/"):
        url = url[:-1]
    return url.strip()


def get_domain(url):
    parsed_uri = urltools.split(url)
    return parsed_uri.netloc


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def parse_robots(base_url, robots_txt):
    disallowed = []
    all_agents = False
    user_agent = "User-agent:"
    disallow = "Disallow:"
    for line in robots_txt.split("\n"):
        if line.startswith(user_agent):
            if line.split(user_agent)[1].strip() == "*":
                all_agents = True
            else:
                all_agents = False
        if all_agents and line.startswith(disallow):
            disallow = line.split(disallow)[1].strip()
            disallow = urljoin(base_url, disallow)
            # TODO url canonicalize, add trailing slash, etc...
            disallowed.append(disallow)
    return disallowed


def parse(browser):
    urls = []
    img_urls = []
    title = browser.title

    # TODO also find elements with onClick links?
    # Only need to check if onClick tag has: location.href or document.location
    links = browser.find_elements_by_tag_name("a")
    for link in links:
        ref = link.get_attribute("href")
        if ref is not None:
            # TODO fix canonicalization with new rules from discord image
            # https://ucilnica.fri.uni-lj.si/pluginfile.php/98677/mod_label/intro/Web%20crawling%20-%20basics.pdf?time=1550779699177
            # slide 16
            # ref = canonical(ref)
            urls.append(ref)
    images = browser.find_elements_by_tag_name("img")
    for image in images:
        src = image.get_attribute("src")
        if src is not None:
            # TODO fix canonicalization with new rules from discord image
            # src = canonical(src)
            img_urls.append(src)
    return title, urls, img_urls
