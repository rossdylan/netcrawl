"""
Split up the internet into a series of chunks
"""

from RedisQueue import RedisQueue
from time import sleep


class Chunker(object):
    def __init__(self, redis_host):
        self.work_queue = RedisQueue(redis_host, "inqueue")

    def run(self):
        chunk_id = 0
        for a in range(1, 255):
            for b in range(1, 255):
                for c in range(1, 255):
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
