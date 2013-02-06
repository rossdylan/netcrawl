import chunker
import scanner
import receiver
import spider
import sys

def run_scanner():
    s = scanner.Scanner(sys.argv[1])
    s.run()


def run_chunker():
    c = chunker.Chunker(sys.argv[1])
    c.run()


def run_receiver():
    r = receiver.Receiver(sys.argv[1])
    r.run()

def run_dump():
    r = receiver.Receiver(sys.argv[1])
    r.run_dump()

def run_test():
    c = chunker.Chunker(sys.argv[1])
    c.run_test()

def run_spider():
    sp = spider.Spider(sys.argv[1])
    sp.run()
