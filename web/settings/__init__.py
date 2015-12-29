from global_settings import settings as GLOBAL

FLASKCONFIG = 'flaskconfig'

APPLICATIONS = (
    'mainpage', 
)

DEFAULT_HEADERS = {
    'server' : 'myTaxi WEB Server',
}

try:
    from local import *
except Exception as err:
    print "ERRRR %s" % err
    pass

