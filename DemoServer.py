__author__ = 'Dawson Valdes'

import json
import socket
from datetime import time

from daisycutter.DaisyCutter import DaisyCutter
from daisycutter.DaisyCutter import Handler
from daisycutter.DaisyCutter import Distributor


# demo use case

# DaisyCutter request function always gets passed a bytearray and must return a string
def check_time(data):
    tr = time()
    req_obj = json.loads(data)
    req_obj['time_received'] = tr.isoformat()
    return json.dumps(req_obj)


socket_family = socket.AF_INET
socket_type = socket.SOCK_STREAM
host_ip = "127.0.0.1"
host_port = 1489
socket_buffer = 10

dist_type = Distributor.queued
hand_type = Handler.pooled
size = 1

print(" binding to {0} : {1}".format(host_ip, host_port))
print(" starting a {0} server, listening for {1} connections".format(socket_family.__str__(), socket_type.__str__()))

dc = DaisyCutter(check_time, socket_family, socket_type, dist_type, hand_type, size)
dc.deploy(host_ip, host_port, socket_buffer)