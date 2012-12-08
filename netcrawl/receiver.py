"""
Listen on the outqueue and display the results as they come in
"""
from RedisQueue import RedisQueue
from pprint import pprint


class Receiver(object):
    def __init__(self, redis_host):
        self.output_queue = RedisQueue(redis_host, "outqueue")

    def run(self):
        while True:
            result = self.output_queue.get().data
            pprint(result)
            print "---"
