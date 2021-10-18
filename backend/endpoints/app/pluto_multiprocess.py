import logging as log
import time, platform
import multiprocessing
from multiprocessing import Process, Queue
from threading import Thread

# For local development on Macs
if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")

multiprocess_queue = Queue()


def consume_queue(queue):
    while not queue.empty():
        func, *args = queue.get_nowait()
        try:
            func(*args)
        except Exception as e:
            log.error(e)


# Loop forever and kick up a new process to consume contents of queue
def create_queue_processes(queue):
    while True:
        if queue.empty():
            time.sleep(0.2)
            continue
        p = Process(target=consume_queue, args=(queue,))
        p.start()
        p.join()


def start_processor_thread():
    t = Thread(target=create_queue_processes, args=(multiprocess_queue,))
    t.daemon = True
    log.info("Starting the queue processes creation daemon thread...")
    t.start()


def execute_in_child_process(func, *args):
    multiprocess_queue.put((func, *args))


