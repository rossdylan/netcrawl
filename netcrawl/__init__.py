import chunker
import scanner
import receiver
import crawler


def run_scanner():
    s = scanner.Scanner("localhost")
    s.run()


def run_chunker():
    c = chunker.Chunker("localhost")
    c.run()


def run_receiver():
    r = receiver.Receiver("localhost")
    r.run()

def run_dump():
    r = receiver.Receiver("localhost")
    r.run_dump()

def run_test():
    c = chunker.Chunker("localhost")
    c.run_test()

def run_crawler():
    cr = crawler.Crawler("localhost")
    cr.run()
