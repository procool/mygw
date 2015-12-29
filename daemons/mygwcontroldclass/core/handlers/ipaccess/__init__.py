import json
import tornado.web
import os, sys
import logging

from decorators import returnstatus

from models.session import session
from models.base import get_model

InetEther = get_model('inet_ether.InetEther')

from libs.pfctl import PFCtl


class ipAccessHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    @returnstatus
    def get(self, ip):
        logging.debug('REQUEST: %s' % self.request.body)
        client = session.query(InetEther).filter(InetEther.is_active==True)
        client = client.filter(InetEther.ip==ip).first()

        if client is None:
            return 404

        proxy = None
        if client.access_type in PFCtl.ip_proxy_types:
            proxy = PFCtl.ip_proxy_types[client.access_type]
        PFCtl.set_ip_proxy(client.ip, proxy)

        return {'ip': ip, 'access': client.access_type,}
        ##return 400


    def post(self):
        return self.get()
 

    def write_error(self, status_code, body=None, **kwargs):
        if body is None:
            return super(ipAccessHandler, self).write_error(status_code, **kwargs)
        self.set_header('Server', self.application.server.engine.server_name)

        self.write(body)


