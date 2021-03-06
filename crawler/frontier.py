import collections


class Frontier:
    request_history = dict()

    def __init__(self, starting_urls=None, site_robots=None):
        if not starting_urls:
            starting_urls = []
        if not site_robots:
            site_robots = dict()

        # Robots.txt parsed with urllib.robotsparser and stored to site_robots
        self.site_robots = site_robots

        # Used to forever know with what urls we started this instance
        self.starting_urls = starting_urls.copy()

        self.url_queue = starting_urls

    def can_fetch(self, site_id, url):
        """
            Important note: robotsparser has a problem while creating rules for wildcard parameters (*, $), example: *?bold_mode*
        """
        rp = self.site_robots.get(site_id)
        if rp:
            return rp.can_fetch("wier-spider", url)

        return True

    def add_url(self, url):
        self.url_queue.insert(0, url)

    def get_url(self):
        if self.url_queue:
            return self.url_queue.pop(0)
        else:
            return None

    def add_site_robots(self, site_id=None, rp=None):
        if self.site_robots.get(site_id):
            print(f"Something went wrong, site {site_id} robots parser already exists.")

        self.site_robots[site_id] = rp

    def check_duplicates(self):
        duplicates = [item for item, count in collections.Counter(self.url_queue).items() if count > 1]
        return duplicates
