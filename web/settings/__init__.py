from global_settings import settings as GLOBAL

FLASKCONFIG = 'flaskconfig'

APPLICATIONS = (
    'mainpage', 'cabinet',
)

DEFAULT_HEADERS = {
    'server' : 'myGW WEB Server',
}

try:
    from local import *
except Exception as err:
    print "ERRRR %s" % err
    pass

