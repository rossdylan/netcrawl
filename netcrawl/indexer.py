from RedisQueue import RedisQueue
import pyelasticsearch
import nltk
from nltk.collocations import *
from itertools import chain
import string


def prepareHTML(html):
    text = nltk.clean_html(html)
    for p in string.punctuation + "\n":
        text.replace(p, "")
    words = nltk.word_tokenize(text.lower())
    return words


def genTags(html):
    words = prepareHTML(html)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(words)
    return list(chain.from_iterable(finder.nbest(bigram_measures.pmi, 15)))


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




