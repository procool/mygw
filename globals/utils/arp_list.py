import subprocess
import re

re_arp = re.compile(r'(.*?)\s+.*?((?:[0-9]{1,3}.){3}[0-9]{1,3}).*?((?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})')

def get_arp_list(iface=None):
    """
    Returns iter of clients list: [NAME, IP, MAC]
    """
    args = ['-a']
    if iface is not None:
        args.append('-i %s' % iface)
    cmd = 'arp %s' % " ".join(args)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)

    for line_ in proc.stdout.xreadlines():
        try: 
            yield list(re_arp.findall(line_)[0])
        except:
            continue
        #finally:
        #    raise ValueError


def get_mac_by_ip(ip, iface=None):
    clients = get_arp_list(iface=iface)
    for cli in clients:
        if cli[1] == ip:
            try: clients.close()
            except: pass
            del clients
            return cli[2]
     

if __name__ == '__main__':

    for client in get_arp_list('re1'):
        print "RES: ", client



