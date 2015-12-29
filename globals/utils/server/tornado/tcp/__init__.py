# -*- coding: utf-8 -*-
# vim: set expandtab shiftwidth=4:

__import__('gevent.monkey').monkey.patch_all()

import time
import logging
import threading

from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer

from daemon.simpledaemon import SimpleDaemon
from utils.server.tornado import TornadoDaemonBackend


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

## New connection activity:
class newConnection(object):

    stream_set = set([])

    def __init__(self, server, stream, address, commands=None):
        logging.debug('Receive a new connection from %s', address)
        self.server = server
        self.stream = stream
        self.address = address
        self.commands = commands
        self.stream_set.add(self.stream)
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\n', self._on_read_line)

    def _on_read_line(self, data):
        logging.info('Command from %s: %s' % (self.address, data))
        #for stream in self.stream_set:
        #    stream.write(data, self._on_write_complete)

        if self.commands is not None:
            self.commands.process(self, data)

    ## Write answer complete, wait for another command:
    def _on_write_complete(self):
        logging.info('Write answer to %s', self.address)
        if not self.stream.reading():
            self.stream.read_until('\n', self._on_read_line)

    def _on_close(self):
        logging.info('client quit %s', self.address)
        self.stream_set.remove(self.stream)

    def write(self, data, on_complete=None):
        self.stream.write(data, on_complete)



def background(f):
    """
    a threading decorator
    use @background above the function you want to thread
    (run in the background)
    """
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f



class TornadoTCPDaemonServer(TCPServer):

    port = 5555 ## Default port
    host = None
    commands = None

    def __init__(self, io_loop=None, ssl_options=None, **kwargs):
        io_loop = io_loop or IOLoop.instance()
        self.is_exit = False
 
        super(TornadoTCPDaemonServer, self).__init__(io_loop=io_loop, ssl_options=ssl_options, **kwargs)

    def handle_stream(self, stream, address):
        newConnection(self, stream, address, self.commands)

    def run_every_time(self):
        while True:
            if self.is_exit:
                break
            time.sleep(1)

    def stop(self):
        self.is_exit = True




class TornadoTCPDaemonBackend(TornadoDaemonBackend):


    def __init__(self, server):
        self.server_class = server

    @background
    def run_every_time(self):
        self.server.run_every_time()

    def run(self):

        self.server = self.server_class()
        largs = {}
        if self.server_class.host is not None:
            largs['address'] = self.server_class.host
        self.server.listen(self.server_class.port, **largs)
        logging.info("Listen TCP: %s:%s" % (self.server_class.host, self.server_class.port))

        self.run_every_time()

    def stop(self):
        self.server.stop()









