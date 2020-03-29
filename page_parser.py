from url_normalize import url_normalize
from urllib.parse import urlparse


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
    parsed_uri = urlparse(url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return canonical(result)


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.hostname}/'.format(uri=parsed_uri)


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
            disallowed.append(base_url + line.split(disallow)[1].strip())
    return disallowed


def parse(browser):
    urls = []
    img_urls = []
    title = browser.title

    # TODO also find elements with onClick links?
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
