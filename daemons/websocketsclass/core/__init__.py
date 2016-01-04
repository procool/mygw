import copy
import time
import logging

import tornado.web

from handlers.root import rootHandler
from handlers.messages import messagesHandler

globals = {
}

application = tornado.web.Application([

    (r"/", rootHandler, globals),
    (r"/messages/", messagesHandler, globals),

])




class coreEngine(object):

    def __init__(self, server):
        self.server = server



    def run_every_time(self):
        pass






