from RedisQueue import RedisQueue
from bs4 import BeautifulSoup
from pprint import pprint, pformat
import requests


class WebPage(object):
    def __init__(self, html, ip, port):
        self.ip = ip
        self.port = port
        self.html = html
        soup = BeautifulSoup(self.html)
        a_tags = soup.find_all('a')

        all_links = map(lambda l: l.get('href'),a_tags)
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

    def __repr__(self):
        return "{0}:{1}\n{2}".format(
                self.ip,
                self.port,
                pformat(self.links))


class Crawler(object):
    def __init__(self, redis_host):
        self.output_queue = RedisQueue(redis_host, "outqueue")
        self.pages_queue = RedisQueue(redis_host, "pagesqueue")

    def run(self):
        while True:
            result = self.output_queue.get().data
            print "Processing: {0}".format(result['ip'])
            open_ports = filter(lambda p: p['state']=='open',result['ports'])
            web_ports = filter(lambda p: p['num'] != '21', open_ports)
            pages = []
            if web_ports != []:
                for port_dict in web_ports:
                    port = int(port_dict['num'])
                    if port == 443:
                        try:
                            response = requests.get("https://{0}:{1}".format(
                                result['ip'],
                                port))
                        except:
                            pass
                    else:
                        response = requests.get("http://{0}:{1}".format(
                            result['ip'],
                            port))
                    if response.status_code == 200:
                        pages.append(WebPage(response.text, result['ip'],port))
            pprint(pages)
            print "---"





