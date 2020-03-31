class Frontier:
    request_history = {}

    def __init__(self, starting_urls=None, disallowed_urls=None):
        if not starting_urls:
            starting_urls = []
        if not disallowed_urls:
            disallowed_urls = []

        # Used to forever know with what urls we started this instance
        self.starting_urls = starting_urls.copy()

        self.disallowed_urls = disallowed_urls
        self.url_queue = starting_urls

    def add_disallowed_urls(self, urls):
        # TODO maybe use set instead of array
        for url in urls:
            if url not in self.disallowed_urls:
                self.disallowed_urls.append(url)

    def allowed(self, url):
        return url not in self.disallowed_urls

    def add_url(self, url):
        self.url_queue.append(url)

    def get_url(self):
        if self.url_queue:
            return self.url_queue.pop(0)
        else:
            return None
