def parse(browser):
    urls = []
    img_urls = []

    links = browser.find_elements_by_tag_name("a")
    for link in links:
        ref = link.get_attribute("href")
        if ref is not None:
            urls.append(ref)
    images = browser.find_elements_by_tag_name("img")
    for image in images:
        src = image.get_attribute("src")
        if src is not None:
            img_urls.append(src)
    return urls, img_urls
