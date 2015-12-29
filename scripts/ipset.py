#!/usr/bin/env python

import sys
import subprocess

import cron.py_path
from global_settings import Settings

settings = Settings()

proxylist = [
    'rdr_tor',
    'rdr_proxy',
]

if __name__ == '__main__':
    cmd = 'pfctl -t %(table)s -T %(command)s %(ip)s'
    try: ip = sys.argv[1]
    except:
        print "Usage: %s IP [LIST_NAME]\n" % sys.argv[0]
        print "Avalible lists: \n	%s\n" % "\n	".join(proxylist)
        exit(0)
    try: proxy = sys.argv[2]
    except: proxy = ''
    for p in proxylist:
        params = { 
            'table': p,
            'command': 'delete',
            'ip': ip,
        }

        if p == proxy:
            params['command'] = 'add'

        cmd_ = cmd % params
        print "DEBUG:", cmd_
        subprocess.Popen(cmd % params, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)




