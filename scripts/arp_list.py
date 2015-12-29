#!/usr/bin/env python

import cron.py_path
from utils.arp_list import get_arp_list


for client in get_arp_list('re1'):
    print "RES: ", client

