__author__ = 'dawsonvaldes'
from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import Pipe

from daisycutter.distributors.BaseDistributor import BaseDistributor
from daisycutter.workers.PipedWorker import PipedWorker


class PipedDistributor(BaseDistributor):
    def __init__(self, socket_handler):
        BaseDistributor.__init__(self, socket_handler)
        self.connection_workers_pipes = list()
        self.connection_workers_locks = list()
        self.pipe_position = 0

    def new_worker(self):
        new_lock = Lock()
        new_pipe_receive, new_pipe_send = Pipe(False)
        self.connection_workers_pipes.append(new_pipe_send)
        self.connection_workers_locks.append(new_lock)
        return Process(target=PipedWorker, args=(self.socket_handler, new_pipe_receive, new_lock))

    def delete_worker(self, index):
        super(PipedDistributor, self).delete_worker(index)
        self.connection_workers_pipes.pop(index)
        self.connection_workers_locks.pop(index)

    def process_handel(self, socket_handel):
        if self.pipe_position >= len(self.connection_workers_pool):
            self.pipe_position = 0
        self.connection_workers_locks[self.pipe_position].aquire()
        self.connection_workers_pipes[self.pipe_position].send(socket_handel)
        self.connection_workers_locks[self.pipe_position].release()