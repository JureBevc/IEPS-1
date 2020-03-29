from url_normalize import url_normalize
from urllib.parse import urlparse


def canonical(url):
    url = url.split("?")[0]
    url = url.split("#")[0]
    url = url_normalize(url)

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


def parse_robots(domain, robots_txt):
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
            disallowed.append(domain + line.split(disallow)[1].strip())
    return disallowed


def parse(browser):
    urls = []
    img_urls = []
    title = browser.title

    links = browser.find_elements_by_tag_name("a")
    for link in links:
        ref = link.get_attribute("href")
        if ref is not None:
            ref = canonical(ref)
            urls.append(ref)
    images = browser.find_elements_by_tag_name("img")
    for image in images:
        src = image.get_attribute("src")
        if src is not None:
            img_urls.append(src)
    return title, urls, img_urls
