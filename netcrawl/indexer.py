from RedisQueue import RedisQueue
import pyelasticsearch
import nltk
from nltk.collocations import *


def genTags(html):
    text = nltk.clean_html(html)
    bigram_measures = nltk.collections.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(3)
    return finder.nbest(bigram_measures.pmi, 5)


class Indexer(object):
    def __init__(self, redis_host, es_urls):
        self.pages_queue = RedisQueue(redis_host, "pagesqueue") # take pages out of this queue
        self.links_queue = RedisQueue(redis_host, "linksqueue") # put links into this queue
        self.connection = pyelasticsearch.ElasticSearch(es_urls)
        try:
            self.connection.create_index("webpages")
        except:
            pass

    def run(self):
        while True:
            result = self.pages_queue.get().data
            result['tags'] = genTags(result['html'])
            self.connection.index('webpages', 'webpage', result, id=result['ip'])
            print('Indexed {0}'.format(result['ip']))
            for link in result['links']:
                self.links_queue.put(link)




