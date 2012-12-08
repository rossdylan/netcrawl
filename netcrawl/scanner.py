class NmapResult(object):
    """
    Class to hold the results of an nmap scan
    """
    def __init__(self, xml):
        pass
class RedisQueue(object):
    def __init__(self, host, channel):
        self.host = host
        self.channel = channel
class Scanner(object):
    """
    Get an item from a queue, scan it, and send the results to the output queue
    """
    def __init__(self, redis_host, in_queue, out_queue):
        self.redis_host = redis_host
        self.scan_params = "nmap -f --randomize-hosts -g 21 -sS -p21,80,443,8000,8080 -oX - -D RND,RND,RND,RND,RND,RND,RND --privileged"
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            pass

