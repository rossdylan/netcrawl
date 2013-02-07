import requests
from RedisQueue import RedisQueue
from model import WebPage

goodExtensions = ['php','txt','html','py','xhtml','xml','atom','rss','htm','js']

class Crawler(object):
    def __init__(self, redis_host, depth=10):
        self.links_queue = RedisQueue(redis_host, "linksqueue")
        self.pages_queue = RedisQueue(redis_host, "pagesqueue")

    def run(self):
        while True:
            link = self.links_queue.get().data
            try:
                page = WebPage(requests.get(link).text, link, 80)
            except:
                print("Exception GETing {0}".format(link))
            self.pages_queue.put(page.to_dict())


