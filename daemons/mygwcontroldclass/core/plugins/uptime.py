import logging
import subprocess
import os

from base import Extention

class upTime(Extention):
    enabled=True
    timeout=20
    cmd='uptime'

    @classmethod
    def get_uptime(cls, engine):
        proc = subprocess.Popen(cls.cmd, shell=True, stdout=subprocess.PIPE)
        answ = proc.stdout.readline()
        over = os.getloadavg()
        logging.info("UPTIME: %s" % answ)
        logging.info("OVER: %s" % str(over))



    @classmethod
    def start(cls, engine):
        cls.get_uptime(engine)
