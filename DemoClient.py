__author__ = 'dawson valdes'
import json
import socket
from datetime import time
from threading import Thread


class client_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.time_data = {'time_begin': '', 'time_end': '', 'time_received': ''}

    def start(self):
        tb = time()
        self.time_data['time_begin'] = tb.isoformat()
        json_data = json.dumps(self.time_data)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 1489))
        client_socket.send(json_data)
        json_data = client_socket.recv(4096)
        self.time_data = json.loads(json_data)
        te = time()
        self.time_data['time_end'] = te.isoformat()


num_threads = 100
thread_list = list()

# init client threads
for a in range(num_threads):
    new_thread = client_thread()
    thread_list.append(new_thread)

# run client threads
for b in thread_list:
    b.start()

# print time data
for c in thread_list:
    c.join()
    print(str(c.time_data))