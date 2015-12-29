import copy
import time
import logging

import tornado.web

from handlers.root import rootHandler
from handlers.ipaccess import ipAccessHandler
from handlers.system import systemHandler

globals = {
}

application = tornado.web.Application([
    (r"/", rootHandler, globals),
    (r"/ip/([\d.]+)/access/", ipAccessHandler, globals),
    (r"/system/([\d\w]+)/", systemHandler, globals),

])


class coreEngine(object):

    server_name = 'myGW Control Server'

    def __init__(self, server):
        self.server = server

    def run_every_time(self):
        pass






