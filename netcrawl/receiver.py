"""
Listen on the outqueue and display the results as they come in
"""
from RedisQueue import RedisQueue
from pprint import pprint, pformat


class Receiver(object):
    def __init__(self, redis_host):
        self.output_queue = RedisQueue(redis_host, "outqueue")

    def run(self):
        while True:
            result = self.output_queue.get().data
            pprint(result)
            print "---"

    def run_dump(self):
        dumpfile = open("netcrawl.log", "w")
        while True:
            result = self.output_queue.get().data
            pprint(result)
            dumpfile.write(dumpfile)
            dumpfile.flush()
