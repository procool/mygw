import copy
import time
import logging

import tornado.web

from utils.plugins import Plugins
from utils.myredis import myRedis, Message as RedisMSG

from handlers.root import rootHandler
from handlers.ipaccess import ipAccessHandler
from handlers.system import systemHandler

from libs.pfctl import PFCtl

Plugins.init('mygwcontroldclass/core/plugins')



globals = {
}

application = tornado.web.Application([
    (r"/", rootHandler, globals),
    (r"/ip/([\d.]+)/access/", ipAccessHandler, globals),
    (r"/system/([\d\w]+)/", systemHandler, globals),

])


class coreEngine(object):

    server_name = 'myGW Control Server'
    redis = myRedis(instance='mygwcontrold', channel='status_channel')

    def __init__(self, server):
        self.server = server
        self.tasks = []
        self.plugins = Plugins

        for ext_ in Plugins.get_enabled_extensions():
            try: ext_().init(self)
            except: pass

    @classmethod
    def logaction(cls, **kwargs):
        data = {
            'owner': 'mygwcontrold',
            'ident': 'undefined',
        }
        data.update(kwargs)
        cls.redis.send(RedisMSG(**data))
        return True


    def add_task(self, task, **details):
        self.tasks.append([task, details])
    
    def run_every_time(self):

        ## Exec tasks:
        tasks, self.tasks = self.tasks, []
        for task, details in tasks:
            logging.info("Running task: %s: %s" % (task, details))
            try: task()
            except Exception as err:
                logging.error("Error on exec task: %s: %s" % (task, err))

        for ext_ in Plugins.get_enabled_extensions():
            try: ext_().run_once(self)
            except Exception as err:
                if not hasattr(ext_, 'errors'):
                    ext_.errors = 0
                ext_.errors += 1
                logging.error('Plugin: "%s" Extention: "%s" error: %s' % (ext_.filename, ext_.name, err))
                if ext_.errors > 5:
                    logging.error('Plugin: "%s" Extention: "%s" disabling...' % (ext_.filename, ext_.name))
                    ext_.enabled = False





