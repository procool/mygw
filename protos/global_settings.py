TIMEDIFF_TZ = int(@TIMEDIFF_TZ@)

IF_INT            = '@IF_INT@'
IP_INT            = '@IP_INT@'
NET_INT           = '@NET_INT@'

IF_EXT            = '@IF_EXT@'
IP_EXT            = '@IP_EXT@'


DATABASES = {
    'default': {
        'URI': '@DB_TYPE_IDENT@://@DB_USER@:@DB_PASS@@@DB_HOST@:@DB_PORT@/@DB_NAME@',
        'SA': { 
            'echo': True,
            'pool_size': 10,
            'pool_recycle':10,
            ##'pool_recycle': 7200,

        },
    },
}

if len('@DB_SOCKET@') > 0:
    DATABASES['default']['URI'] += '?unix_socket=@DB_SOCKET@'


