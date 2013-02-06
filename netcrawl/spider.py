from RedisQueue import RedisQueue
import requests
from model import WebPage


class Spider(object):
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
