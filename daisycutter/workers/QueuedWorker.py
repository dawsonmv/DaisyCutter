__author__ = 'dawsonvaldes'

from daisycutter.workers.BaseWorker import BaseWorker


class QueuedWorker(BaseWorker):
    def __init__(self, sh, hq, qc):
        BaseWorker.__init__(self, sh)
        self.handel_queue = hq
        self.queue_condition = qc

    def get_handel(self):
        self.queue_condition.acquire()
        self.queue_condition.wait()
        if self.handel_queue.empty():
            self.queue_condition.notify()
            self.queue_condition.release()
            return None
        else:
            handel = self.handel_queue.get()
            self.queue_condition.notify()
            self.queue_condition.release()
            return handel