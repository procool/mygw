#!/usr/bin/env python

import logging
import subprocess
from sqlalchemy import func, and_, or_, not_

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')
##logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%d/%b/%Y %H:%M:%S]')

import cron.py_path
from models.session import session
from models.base import get_model

InetEther = get_model('inet_ether.InetEther')

from libs.pfctl import PFCtl

def process_clients():
    clients = session.query(InetEther).filter(InetEther.is_active==True)
    for cli in clients:
        proxy = None
        if cli.access_type in PFCtl.ip_proxy_types:
            proxy = PFCtl.ip_proxy_types[cli.access_type]
        PFCtl.set_ip_proxy(cli.ip, proxy)



if __name__ == '__main__':
    process_clients()







