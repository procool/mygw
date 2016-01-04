import os, sys, fcntl
import time
import logging

class tailF(object):

    def __init__(self, name):
        self.name = name
        self.fd = open(name)
        #fcntl.fcntl(self.fd.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        fsize = self.fd.tell() 
        ##self.fd.seek(0, 0) 
        self.fd.seek(0, 2) 
        self.p = self.fd.tell()
        #self.p = 0

    def xreadlines(self):
        while True:
            self.fd.seek(self.p)
            latest_data = self.fd.read()
            self.p = self.fd.tell()
            if latest_data:
                lines = latest_data.split('\n')
                for line in lines:
                    yield line.strip()
            time.sleep(0.1)

if __name__ == '__main__':
    fl = sys.argv[1]
    tf = tailF(fl)
    for line in tf.xreadlines():
        print line



