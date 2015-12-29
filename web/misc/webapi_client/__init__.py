import re 

from flaskcbv.conf import settings

from misc.httpclient import httpClient


re_session = re.compile(r"session=(.*?);")

class webapiClient(httpClient):
    host = settings.WEBAPI_HOST
    port = settings.WEBAPI_PORT

    def __check_session(self, r):
        try: self.set_session(re_session.findall(r.headers['set-cookie'])[0])
        except: self.__session = None

    def isauthed(self, sessionid):
        try: r, b = self.call_handler('tests/isauthed', session=sessionid)
        except Exception as err:
            ##print err, dir(err), err.code
            return False
        self.__check_session(r)
        return True

    def profile(self, **kwargs):
        r, b = self.call_handler('contacts/profile/', **kwargs)
        self.__check_session(r)
        return b

    def orders_list(self, **kwargs):
        r, b = self.call_handler('orders/my/list/', **kwargs)
        self.__check_session(r)
        return b


    def order_details(self, order_id, **kwargs):
        r, b = self.call_handler('orders/%s/' % order_id, **kwargs)
        self.__check_session(r)
        return b



