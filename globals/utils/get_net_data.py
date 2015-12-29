#!/usr/bin/env python

import sys
from ipmask import NetData

if __name__ == "__main__":
    
    addr_ = sys.argv[1]
    type_ = sys.argv[2]
    
    addr, cidr = addr_.split('/')
    n = NetData(addr, cidr)

    if type_ == 'addr':
        print n.addr,
    elif type_ == 'mask':
        print n.mask,
    elif type_ == 'net':
        print n.net,
    elif type_ == 'broadcast':
        print n.broadcast,
    elif type_ == 'range':
        print n.range,
    elif type_ == 'cidr':
        print n.cidr,


