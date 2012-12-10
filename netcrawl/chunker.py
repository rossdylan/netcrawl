"""
Split up the internet into a series of chunks
"""

from RedisQueue import RedisQueue
from time import sleep
from random import shuffle

class Chunker(object):
    def __init__(self, redis_host):
        self.work_queue = RedisQueue(redis_host, "inqueue")

    def run(self):
        chunk_id = 0
        for a in shuffle(range(1, 255)):
            for b in shuffle(range(1, 255)):
                for c in shuffle(range(1, 255)):
                    ip_range = "{0}.{1}.{2}.0/24".format(a, b, c)
                    print "Sending chunk {0} range: {1}".format(chunk_id,
                            ip_range)
                    task = {
                            "range": ip_range,
                            "id": chunk_id
                           }
                    self.work_queue.put(task)
                    chunk_id += 1
                    sleep(10)
    def run_test(self):
        self.work_queue.put({"range": "129.21.50.0/24", "id":0})
