from pprint import pformat
from bs4 import BeautifulSoup


class WebPage(object):
    def __init__(self, html, ip, port):
        self.ip = ip
        self.port = port
        self.html = html
        soup = BeautifulSoup(self.html)
        a_tags = soup.find_all('a')

        all_links = map(lambda l: l.get('href'), a_tags)
        all_links = filter(lambda l: l != None, all_links)
        relative_links = filter(lambda l: l.startswith("/"), all_links)
        other_thinks = filter(lambda l: not l.startswith("/"), all_links)
        self.links = other_thinks

        self.links.extend(map(
                lambda l: "{0}:{1}{2}".format(
                    self.ip,
                    self.port,
                    l),
                relative_links))
        print "Scraped {0} links from {1}:{2}".format(
                len(self.links),
                self.ip,
                self.port)

    def to_dict(self):
        return {
                'ip': self.ip,
                'port': self.port,
                'html': self.html,
                'links': self.links
               }

    def __repr__(self):
        return "{0}:{1}\n{2}".format(
                self.ip,
                self.port,
                pformat(self.links))


