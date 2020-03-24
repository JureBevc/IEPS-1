class Frontier:
    url_queue = []

    def __init__(self, starting_urls):
        for url in starting_urls:
            self.add_url(url)

    def add_url(self, url):
        self.url_queue.insert(0, url)

    def get_url(self):
        if len(self.url_queue) > 0:
            return self.url_queue.pop()
        else:
            return None
