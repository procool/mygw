import logging
import gevent

from utils.tail_f import tailF
from base import Extention


class logsMessages(Extention):
    enabled=True
    fname='/var/log/messages'
    proc = None


    @classmethod
    def init(cls, engine):
        cls.engine = engine
        gevent.spawn(cls.process_lines)

    @classmethod
    def check_for_log(cls):
        cls.proc = tailF(cls.fname)
        ##fcntl.fcntl(cls.proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)


    @classmethod
    def process_lines(cls):
        while True:
            cls.check_for_log()
            for line in cls.proc.xreadlines():
                cls.engine.logaction(ident='plugin_messages', line=line)
                gevent.sleep(0.1)
            cls.proc = None
            gevent.sleep(5)
        
    

