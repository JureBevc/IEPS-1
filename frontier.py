class Frontier:
    url_queue = []
    disallowed_urls = []
    request_history = {}

    def __init__(self, starting_urls):
        for url in starting_urls:
            self.add_url(url)

    def add_disallowed_urls(self, urls):
        for url in urls:
            if url not in self.disallowed_urls:
                self.disallowed_urls.append(url)

    def allowed(self, url):
        return url not in self.disallowed_urls

    def add_url(self, url):
        self.url_queue.insert(0, url)

    def get_url(self):
        if len(self.url_queue) > 0:
            return self.url_queue.pop()
        else:
            return None
