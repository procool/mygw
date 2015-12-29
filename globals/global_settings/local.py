TIMEDIFF_TZ = int("3")

IF_INT            = 're1'
IP_INT            = '10.3.2.1'
NET_INT           = '10.3.2.1/24'

IF_EXT            = 're0'
IP_EXT            = 'DHCP'


DATABASES = {
    'default': {
        'URI': 'mysql://root:@localhost:3306/mygw',
    },
}

if len('/tmp/mysql.sock') > 0:
    DATABASES['default']['URI'] += '?unix_socket=/tmp/mysql.sock'


