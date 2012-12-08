from retask.task import Task
from retask.queue import Queue


class RedisQueue(object):
    def __init__(self, host, name, port=6379, password=None):
        self.super_queue = Queue(
                name,
                {
                    'host': host,
                    'port': port,
                    'db': 0,
                    'password': password,
                })
        self.super_queue.connect()

    def get(self):
        return self.super_queue.wait()

    def put(self, data):
        self.super_queue.send(Task(data))


