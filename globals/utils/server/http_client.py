import json
from urllib2 import urlopen, HTTPError
from urllib import urlencode

import logging


class HTTPClient(object):

    def __init__(self, host='localhost', port=90):
        self.host = host
        self.port = port

    def get_serv_addr (self):
        return 'http://%s:%s/' % ( self.host, self.port, )
        
            
    def call_handler(self, handler, *args, **kwargs):
        url = '%s%s/' % (self.get_serv_addr(), handler)

        try: postdata = kwargs.pop('postdata')
        except: postdata=None

        for arg in args:
            url += '%s/' % arg
            
        params = urlencode(kwargs)
        url = '%s?%s'% (url, params)
        logging.debug("Request url: %s" % url)

        try: response = urlopen(url, postdata)
        except HTTPError as err:
            raise(err)
        except:
            return None
        
        ## Reading data:
        try:
            response = response.read()
        except:
            return None
        
        ## Decoding to JSON:
        try:
            return json.loads(response)
        except:
            return response


