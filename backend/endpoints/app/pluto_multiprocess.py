import logging as log
import platform
import multiprocessing
from multiprocessing import Process, Pipe
from threading import Thread


# For local development on Macs
if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")


pipe_recv, pipe_send = Pipe()


def consume_pipe(pipe_in):
    while pipe_in.poll(0.2):
        func, *args = pipe_in.recv()
        try:
            print("Execute")
            func(*args)
        except Exception as e:
            log.exception(e)


# Loop forever and kick up a new process to consume contents of queue
def create_queue_processes():
    while True:
        if not pipe.poll(0.2):
            continue
        print("Create process")
        p = Process(target=consume_pipe, args=(pipe,))
        p.start()
        p.join()


def start_processor_thread():
    t = Thread(target=create_queue_processes)
    t.daemon = True
    log.info("Starting the queue processes creation daemon thread...")
    t.start()


def execute_in_child_process(func, *args):
    print("put in child process")
    pipe_recv.send((func, *args))


