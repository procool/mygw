from random import randrange
import logging
import time

class Extention(object):

    enabled=False
    lastupdate = time.time()
    __nextupdate = None
    timeout = 15
    timeout_type = 'rand'

    @classmethod
    def init(cls, engine):
        pass

    @classmethod
    def get_next_update(cls, clear=False):
        if cls.__nextupdate is None or clear:
            timeout = cls.timeout_type == 'rand' and randrange(cls.timeout) or cls.timeout
            cls.__nextupdate = time.time() + timeout
        return cls.__nextupdate

    @classmethod
    def is_ready(cls):
        if cls.get_next_update() < time.time():
            cls.get_next_update(True)
            return True
        return False


    @classmethod
    def run_once(cls, engine):
        if cls.is_ready():
            cls.start(engine)

    @classmethod
    def start(cls, engine):
        pass
