from random import randrange
import time

class Extention(object):

    enabled=False
    lastupdate = time.time()
    __nextupdate = None
    timeout = 15

    @classmethod
    def get_next_update(cls, clear=False):
        if cls.__nextupdate is None or clear:
            cls.__nextupdate = time.time() + randrange(cls.timeout)
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
