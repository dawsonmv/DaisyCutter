__author__ = 'Dawson Valdes'

import socket


class BaseHandler:
    def __init__(self, rf=None, sf=socket.AF_INET, st=socket.SOCK_STREAM):
        self.request_function = rf  # register a request function
        self.socket_family = sf
        self.socket_type = st

    def make_socket(self, h):
        return socket.fromfd(h, self.socket_family, self.socket_type)  # create a socket from file handle

    def get_data(self, s):
        sd = bytearray()  # make a byte array for socket data
        while s.poll():  # while there is something the buffer
            sd.append(s.recv(1024))  # append a byte to the socket data
        s.shutdown(socket.SHUT_RD)  # turn off socket reads
        return sd  # return socket data

    def no_handel(self):
        pass  # what to do if there is no handle

    def handel_socket(self, sh=None):
        if sh is not None:
            cs = self.make_socket(sh)  # connected socket
            rd = self.get_data(cs)  # request data
            fd = self.request_function(rd)  # function data
            cs.send(fd)  # send requested function data to connected socket
            cs.close()  # close connected socket
        else:
            self.no_handel()