
class NetData(object):
    def __init__(self, addr, cidr):
        self.setaddr(addr)
        self.cidr = int(cidr)
        self.set_mask_by_cidr()
        self.set_net()
        self.set_broadcast()

    def setaddr(self, addr):
        self.__addr = map(int, addr.split('.'))

    # Initialize the netmask and calculate based on CIDR mask
    def set_mask_by_cidr(self):
        mask = [0, 0, 0, 0]
        for i in range(self.cidr):
            mask[i/8] = mask[i/8] + (1 << (7 - i % 8))
        self.__mask = mask

    # Initialize net and binary and netmask (net) with addr to get network
    def set_net(self):
        self.__net = []
        for i in range(4):
            self.__net.append(int(self.__addr[i]) & self.__mask[i])


    # Duplicate net into broad array, gather host bits, and generate broadcast
    def set_broadcast(self):
        self.__broadcast = list(self.__net)
        brange = 32 - self.cidr
        for i in range(brange):
            self.__broadcast[3 - i/8] = self.__broadcast[3 - i/8] + (1 << (i % 8))

        # This gives you usable hosts for the given subnet
        xhost = 2 ** brange - 2
        self.range = "{:,}".format(xhost)

    @property
    def addr(self):
        return ".".join(map(str, self.__addr))

    @property
    def mask(self):
        return ".".join(map(str, self.__mask))

    @property
    def net(self):
        return ".".join(map(str, self.__net))

    @property
    def broadcast(self):
        return ".".join(map(str, self.__broadcast))

if __name__ == "__main__":
    addr = raw_input("IP address: ") # need to validate input of IP address 
    cidr = raw_input("CIDR notation, NO / mark!: ")
    n = NetData(addr, cidr)

    # Print information, mapping integer lists to strings for easy printing
    print 'Here are your results:..............'
    print "Address: ", n.addr 
    print "Netmask: " , n.mask
    print "Network: " , n.net
    print "Usable IPs: " , n.range
    print "Broadcast: " , n.broadcast

    raw_input("Press any key to exit...")



