__author__ = 'dawsonvaldes'

import multiprocessing

from daisycutter.handlers.BaseHandler import BaseHandler


class AutoScaledHandler(BaseHandler):
    def __init__(self, f, sf, st):
        BaseHandler.__init__(self, f, sf, st)

    def no_handel(self):
        active_worker = multiprocessing.current_process()
        active_worker.terminate()
