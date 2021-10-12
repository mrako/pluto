import logging as log
import time
import multiprocessing
from multiprocessing import Process, Queue
from queue import Empty
from threading import Thread

multiprocessing.set_start_method("fork")
multiprocess_queue = Queue()


def consume_queue(queue):
    try:
        while True:
            item = queue.get_nowait()
            item()
    except Empty:
        log.debug("Empty queue")


# Loop forever and kick up a new process to consume contents of queue
def create_queue_processes(queue):
    while True:
        if len(queue) == 0:
            time.sleep(0.2)
            continue
        p = Process(target=consume_queue, args=(queue,))
        p.start()
        p.join()


def start_calls_processor_thread():
    t = Thread(target=create_queue_processes, args=(multiprocess_queue,))
    t.daemon = True
    t.start()


def put_in_queue(item):
    multiprocess_queue.put(item)


