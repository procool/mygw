import json
import logging

from urllib2 import urlopen, HTTPError
from urllib2 import build_opener, HTTPCookieProcessor
from urllib import urlencode

from cookielib import CookieJar


class httpClient(object):
    host='localhost'
    port=90

    def __init__(self, host=None, port=None, session=None):
        self.__host = host or self.host
        self.__port = port or self.port
        self.__session = session

    def get_session(self):
        return self.__session

    def set_session(self, session):
        self.__session = session

    def get_serv_addr (self):
        return 'http://%s:%s/' % ( self.__host, self.__port, )


    def call_handler(self, handler, postdata=None, **kwargs):
        url = '%s%s' % (self.get_serv_addr(), handler)

        params = urlencode(kwargs)
        url = '%s?%s'% (url, params)
        logging.debug("Request units url: %s" % url)

        cj = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cj))

        if self.__session is not None:
            opener.addheaders.append(('Cookie', 'session=%s' % self.__session))

        ##try: response = urlopen(url, postdata)
        try: response = opener.open(url, postdata)
        except HTTPError as err:
            raise(err)
        except:
            return None, None

        ## Reading data:
        try:
            body_ = response.read()
        except:
            return None, None

        ## Decoding to JSON:
        try:
            return response, json.loads(body_)
        except:
            return response, body_



