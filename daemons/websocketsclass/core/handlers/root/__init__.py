import os, sys
import logging
import json
import time

import tornado.web

class rootHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('You should use websockets!')



    def post(self):
        return self.get()



