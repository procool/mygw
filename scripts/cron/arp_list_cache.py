#!/usr/bin/env python



import py_path
from utils.arp_list import get_arp_list
from global_settings import settings
from models.session import session
#from models.all_models import Users, InetEther
from models.base import get_model

ARPCache = get_model('arp_cache.ARPCache')

if __name__ == "__main__":
    nlist = []
    for s, ip, mac in get_arp_list('rl0'):
        print "RES: ", ip, mac
        ac = ARPCache(ip=ip, mac=mac)
        nlist.append(ac)
    session.query(ARPCache).filter().delete()
    for ac in nlist:
        session.add(ac)
    session.commit()



