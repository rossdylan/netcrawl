from RedisQueue import RedisQueue
from bs4 import BeautifulSoup
from pprint import pformat
import requests


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


class Crawler(object):
    def __init__(self, redis_host):
        self.output_queue = RedisQueue(redis_host, "outqueue")
        self.pages_queue = RedisQueue(redis_host, "pagesqueue")

    def run(self):
        while True:
            result = self.output_queue.get().data
            open_ports = filter(lambda p: p['state'] == 'open',
                    result['ports'])
            web_ports = filter(lambda p: p['num'] != 21, open_ports)
            print "Processing: {0}".format(result['ip'])
            if web_ports != []:
                for port_dict in web_ports:
                    port = int(port_dict['num'])
                    if port == 443:
                        url_string = "https://{0}:{1}".format(
                                result['ip'],
                                port)
                    else:
                        url_string = "http://{0}:{1}".format(
                                result['ip'],
                                port)

                    try:
                        response = requests.get(url_string, verify=False)
                    except Exception as e:
                        print "Error crawling: {0}:{1} -> {2}".format(
                                result['ip'],
                                port,
                                str(e))

                    if response and response.status_code == 200:
                        page = WebPage(response.text, result['ip'], port)
                        print page
                        if page.links != []:
                            self.pages_queue.put(page.to_dict())
