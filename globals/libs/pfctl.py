import logging
import subprocess

commands = {
    'table': 'sudo pfctl -t %(table)s -T %(command)s %(ip)s',
}

class PFCtl(object):
    
    ## key: name, value: name of PF table
    ip_proxy_types = {
        'tor': 'rdr_tor',
        'squid': 'rdr_squid',
    }


    @classmethod
    def set_ip_proxy(cls, ip, proxy):
        for p in cls.ip_proxy_types.values():
            params = {
                'table': p,
                'command': 'delete',
                'ip': ip,
            }

            if p == proxy:
                params['command'] = 'add'

            cmd_ = commands['table'] % params
            logging.debug('PF: EXECUTING: "%s"' % cmd_)
            subprocess.Popen(cmd_, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,)









