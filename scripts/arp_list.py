#!/usr/bin/env python

import cron.py_path
from utils.arp_list import get_arp_list


for client in get_arp_list('rl0'):
    print "RES: ", client

