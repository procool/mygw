import json
import tornado.web
import os, sys
import logging
import subprocess

from decorators import returnstatus

cmd_shutdown = 'sudo shutdown -%(flag)s %(time)s %(reason)s'


class systemHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    @returnstatus
    def get(self, command):
        logging.debug('REQUEST: %s' % self.request.body)
        if command in ('poweroff', 'reboot'):
            params = {
                'flag': command == 'poweroff' and 'p' or 'r',
                'time': 'now',
                'reason': 'by myGW Control HTTP Server'
            }
            cmd_ = cmd_shutdown % params
            def new_task():
                subprocess.Popen(cmd_, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)
            engine = self.application.server.engine
            engine.add_task(new_task, name='system', command=command)
            return {}

        return 404


    def post(self):
        return self.get()
 

    def write_error(self, status_code, body=None, **kwargs):
        if body is None:
            return super(systemHandler, self).write_error(status_code, **kwargs)
        self.set_header('Server', self.application.server.engine.server_name)

        self.write(body)


