__author__ = 'Dawson Valdes'

# MultiProcessServerFrameWork - autoScaling  by Dawson Valdes
import socket
import enum

from daisycutter.distributors import QueuedDistributor
from daisycutter.distributors import PipedDistributor
from daisycutter.handlers import AutoScaledHandler
from daisycutter.handlers import PooledHandler


class DaisyError():
    def __init__(self, et, em):
        self.error_type = et
        self.error_message = em


class Handler(enum.Enum):
    pooled = 1
    auto = 2


class Distributor(enum.Enum):
    piped = 1
    queued = 2


class DaisyCutter():
    def build_pool(self, size):
        for x in range(size):
            self.distributor.add_worker()

    def __init__(self, r_f=None, s_f=socket.AF_INET, s_t=socket.SOCK_STREAM, d_t=Distributor.queued, h_t=Handler.pooled,
                 p_s=2, a_mn=1, a_mx=8, a_time=100.0):
        self.request_function = r_f
        self.socket_family = s_f
        self.socket_type = s_t
        self.distributor_type = d_t
        self.handler_type = h_t
        self.start_workers = p_s
        self.auto_time = a_time

        if self.handler_type == Handler.auto:
            self.max_workers = a_mx
            self.min_workers = a_mn
            self.handler_function = AutoScaledHandler(self.request_function, self.socket_family, self.socket_type)
        elif self.handler_type == Handler.pooled:
            self.handler_function = PooledHandler(self.request_function, self.socket_family, self.socket_type)
        else:
            self.handler_function = AutoScaledHandler(self.request_function, self.socket_family, self.socket_type)
            print("MUST BE alloc_type MUST BE 'Allocation.pooled' or 'Allocation.auto'")

        if self.distributor_type == Distributor.queued:
            self.distributor = QueuedDistributor(self.handler_function)
        elif self.distributor_type == Distributor.piped:
            self.distributor = PipedDistributor(self.handler_function)
        else:
            self.distributor = QueuedDistributor(self.handler_function)
            print("MUST BE dist_type MUST BE 'Distributor.queued' or 'Distributor.piped'")

        self.build_pool(self.start_workers)

    def deploy(self, server_address, server_port, buffer_size, ):
        def evaluate_pool():
            self.distributor.clean_pool()
            return len(self.distributor.connection_workers_pool)

        def pass_socket():
            client_socket, client_address = server.accept()
            client_handle = client_socket.fileno()
            self.distributor.process_handel(client_handle)

        def server_loop_pooled():
            while True:
                iter_time = 0.0
                while evaluate_pool() < self.start_workers:
                    self.distributor.add_worker()
                while iter_time < self.auto_time:
                    pass_socket()
                    if iter_time < self.auto_time:
                        iter_time += 0.01

        def server_loop_auto_scaling():
            while True:
                iter_time = 0.0
                while evaluate_pool() < self.min_workers:
                    self.distributor.add_worker()
                while iter_time < self.auto_time:
                    pass_socket()
                    if iter_time < self.auto_time:
                        iter_time += 0.01
                        if evaluate_pool() < self.max_workers:
                            self.distributor.add_worker()

        server = socket.socket(self.socket_family, self.socket_type)
        server.set_inheritable(True)
        server.bind((server_address, server_port))
        server.listen(buffer_size)
        if self.handler_type == Handler.pooled:
            server_loop_pooled()
        elif self.handler_type == Handler.auto:
            server_loop_auto_scaling()