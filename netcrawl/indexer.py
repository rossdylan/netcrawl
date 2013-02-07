from RedisQueue import RedisQueue
import pyelasticsearch

class Indexer(object):
    def __init__(self, redis_host, es_urls):
        self.pages_queue = RedisQueue(redis_host, "pagesqueue") # take pages out of this queue
        self.links_queue = RedisQueue(redis_host, "linksqueue") # put links into this queue
        self.connection = pyelasticsearch.ElasticSearch(es_urls)
        self.connection.put_mapping('webpages','webpage', {
            "ip": {"type": "string", "store": "yes"},
            "port": {"type": "integer", "store": "yes"},
            "html": {"type": "string", "store": "yes"},
        })

    def run(self):
        while True:
            result = self.pages_queue.get().data
            self.connection.index('webpages', 'webpage', result, id=result['ip'])
            for link in result['links']:
                self.links_queue.put(link)




