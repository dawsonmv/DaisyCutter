__author__ = 'dawsonvaldes'

from daisycutter.handlers.BaseHandler import BaseHandler


class PooledHandler(BaseHandler):
    def __init__(self, f, sf, st):
        BaseHandler.__init__(self, f, sf, st)
