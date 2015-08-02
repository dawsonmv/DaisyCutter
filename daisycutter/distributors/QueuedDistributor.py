__author__ = 'dawson valdes'
from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Lock
from multiprocessing import SimpleQueue

from daisycutter.distributors.BaseDistributor import BaseDistributor
from daisycutter.workers.QueuedWorker import QueuedWorker


class QueuedDistributor(BaseDistributor):
    def __init__(self, socket_handler):
        BaseDistributor.__init__(self, socket_handler)
        self.socket_queue = SimpleQueue()
        self.queue_condition = Condition(Lock())

    def new_worker(self):
        return Process(target=QueuedWorker, args=(self.socket_handler, self.socket_queue, self.queue_condition))

    def process_handel(self, socket_handel):
        self.queue_condition.acquire()
        self.socket_queue.put(socket_handel)
        self.queue_condition.notify()
        self.queue_condition.release()