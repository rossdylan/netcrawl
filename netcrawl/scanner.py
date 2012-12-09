from subprocess import check_output
from NmapResult import GenerateHosts
from RedisQueue import RedisQueue
import shlex


class Scanner(object):
    """
    Get an item from a queue, scan it, and send the results to the output queue
    """
    def __init__(self, redis_host):
        self.redis_host = redis_host
        self.scan_params = "proxychains nmap -f --randomize-hosts -g 21 -sS -p21,80,443,8000,8080 -oX - -D RND,RND,RND,RND,RND,RND,RND --privileged {0}"
        self.in_queue = RedisQueue(self.redis_host, "inqueue")
        self.out_queue = RedisQueue(self.redis_host, "outqueue")

    def process_chunk(self, data):
        print "Processing chunk {0} range: {1}".format(
                data['id'],
                data['range'])

        result_xml = check_output(
                shlex.split(
                    self.scan_params.format(data.ip_range)))
        hosts = GenerateHosts(result_xml)
        map(lambda h: self.out_queue.put(h.to_dict()), hosts)
        print "Finished processing chunk {0}".format(data['id'])

    def run(self):
        while True:
            nextChunk = self.in_queue.get().data
            self.process_chunk(self, nextChunk)
