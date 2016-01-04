import logging
import subprocess
import os

from base import Extention

class upTime(Extention):
    enabled=True
    timeout=5
    timeout_type=None
    cmd='uptime'

    @classmethod
    def get_uptime(cls, engine):
        proc = subprocess.Popen(cls.cmd, shell=True, stdout=subprocess.PIPE)
        uptime_ = proc.stdout.readline().strip()
        avg = os.getloadavg()
        try:
            idx = uptime_.index(', load averages')
            uptime_ = uptime_[0:idx]
        except: pass
        load_average = {
            0: "%.2f" % avg[0],
            1: "%.2f" % avg[1],
            2: "%.2f" % avg[2],
        }
        engine.logaction(ident='plugin_uptime', uptime=uptime_, load_average=load_average)



    @classmethod
    def start(cls, engine):
        cls.get_uptime(engine)
