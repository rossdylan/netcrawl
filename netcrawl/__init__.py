import chunker
import scanner
import receiver


def run_scanner():
    s = scanner.Scanner("localhost")
    s.run()


def run_chunker():
    c = chunker.Chunker("localhost")
    c.run()


def run_receiver():
    r = receiver.Receiver("localhost")
    r.run()
