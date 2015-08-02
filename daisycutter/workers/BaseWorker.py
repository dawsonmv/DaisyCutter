__author__ = 'Dawson Valdes'

from multiprocessing import Process


class BaseWorker(Process):
    def __init__(self, sh):
        Process.__init__(self)
        self.socket_handler = sh

    def get_handel(self):
        return None

    def run(self):
        while True:
            self.socket_handler.handel_socket(self.get_handel())