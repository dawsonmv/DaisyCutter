__author__ = 'dawsonvaldes'

from daisycutter.workers.BaseWorker import BaseWorker


class PipedWorker(BaseWorker):
    def __init__(self, sh, sp, pl):
        BaseWorker.__init__(self, sh)
        self.socket_pipe = sp
        self.pipe_lock = pl

    def get_handel(self):
        self.pipe_lock.aquire()
        if self.socket_pipe.poll():
            handle = self.socket_pipe.recv()
            self.pipe_lock.release()
            return handle
        else:
            self.pipe_lock.release()
            return None