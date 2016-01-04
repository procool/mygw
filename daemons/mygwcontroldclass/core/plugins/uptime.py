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
        uptime_ = proc.stdout.readline()
        avg = os.getloadavg()
        engine.logaction(ident='plugin_uptime', uptime=uptime_, load_average=avg)



    @classmethod
    def start(cls, engine):
        cls.get_uptime(engine)
