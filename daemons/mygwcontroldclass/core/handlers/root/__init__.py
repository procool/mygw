import json
import tornado.web
import os, sys
import logging

from decorators import returnstatus

class rootHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    @returnstatus
    def get(self):
        logging.debug('REQUEST: %s' % self.request.body)
        return {'test': 'ok'}
        ##return 400


    def post(self):
        return self.get()
 

    def write_error(self, status_code, body=None, **kwargs):
        if body is None:
            return super(rootHandler, self).write_error(status_code, **kwargs)
        self.set_header('Server', self.application.server.engine.server_name)

        self.write(body)


