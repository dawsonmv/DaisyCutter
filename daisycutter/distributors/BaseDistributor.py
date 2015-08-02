__author__ = 'Dawson Valdes'

from multiprocessing import Process


class BaseDistributor:
    def __init__(self, sh):
        self.socket_handler = sh
        self.connection_workers_pool = list()

    def new_worker(self):
        return Process()

    def add_worker(self):
        nw = self.new_worker()
        self.connection_workers_pool.append(nw)
        nw.start()

    def delete_worker(self, index):
        self.connection_workers_pool.pop(index)

    def process_handel(self, socket_handel):
        pass

    def clean_pool(self):
        for zombie in self.connection_workers_pool:
            if not zombie.is_alive():
                self.delete_worker(self.connection_workers_pool.index(zombie))