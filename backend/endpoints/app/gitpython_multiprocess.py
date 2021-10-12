import logging as log
import time
import multiprocessing
from multiprocessing import Process, Queue
from queue import Empty
from threading import Thread

multiprocessing.set_start_method("fork")
multiprocess_queue = Queue()


class ExecutionContext:
    def __init__(self):
        log.debug("Creating context")

    def __enter__(self):
        log.debug("Entering context")

    def __exit__(self):
        log.debug("Destroying execution context")


class Task:
    def __init__(self):
        pass

    # Actual execution happens here, ctx provides e.g. database connections
    def execute(self, ctx, *args):
        pass


def consume_queue(queue, ctx):
    try:
        while True:
            task = queue.get_nowait()
            task.execute(ctx)
    except Empty:
        log.debug("Empty queue")


# Loop forever and kick up a new process to consume contents of queue
def create_queue_processes(queue):
    while True:
        if len(queue) == 0:
            time.sleep(0.2)
            continue
        with ExecutionContext() as ctx:
            p = Process(target=consume_queue, args=(queue, ctx))
            p.start()
            p.join()


def start_calls_processor_thread():
    t = Thread(target=create_queue_processes, args=(multiprocess_queue,))
    t.daemon = True
    t.start()


def put_in_queue(task):
    multiprocess_queue.put(task)


