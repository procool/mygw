import os, sys
import logging
import json
import time
import redis

import tornado.web
import tornado.websocket

from .misc import MessagesCommon, redisChannels

redisChannels.new_message_callback = MessagesCommon.show_message
redisChannels.get_hosts()
redisChannels.set_channels()

redis_ = redis.Redis('localhost')

unauthorized_owners = [
    'websocketsd',
    ##'mygwcontrold',
]


class messagesHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        pass


    def __init__(self, *args, **kwargs):
        self.__session = None
        self.__session_timeout = 5
        self.__session_timeout_ = time.time()
        super(messagesHandler, self).__init__(*args, **kwargs)

        logging.debug("NEW CLIENT: %s" % self)
        MessagesCommon.add_client(self)


    def open(self, channel = ''):
        self.channel = channel


    def handle_request(self, response):
        pass


    def on_message(self, message):
        if not message:
            return
        if len(message) > 10000:
            return
        logging.info('GOT new message from user: %s' % message)
        try: data = json.loads(message)
        except: return
        if not 'command' in data:
            return
        if data['command'] == 'auth':
            if not 'sessionid' in data:
                return
            session_ = data['sessionid']
            if session_ is None:
                self.__session = None
                logging.info('Clear User session!')
                return
            self.__session = session_
            logging.info('GOT User session: %s' % self.__session)
            self.check_session()
            return


    def get_user(self):
        if self.__session is None:
            raise Exception('session is clear')
        key_ = 'mygw_sessions_s2u_%s' % self.__session
        try: return redis_.get(key_)
        except: return None

    def check_session(self):
        try: user_ = self.get_user()
        except: return None
        if user_ is None:
            logging.info('CLEAR Session: %s' % self.__session)
            self.__session = None

    def check_session_by_timeout(self):
        if time.time() > self.__session_timeout + self.__session_timeout_:
            self.check_session()
            self.__session_timeout_ = time.time()

    def show_new_message(self, data, data_raw):
        self.check_session_by_timeout()

        if not 'owner' in data:
            return
        if not data['owner'] in unauthorized_owners and self.__session is None:
            return
        if 'to' in data and data['to'] != self.__session:
            return
        logging.debug('MESSAGE: %s' % data_raw)
        self._show_new_message(data_raw)



    def _show_new_message(self, sdata):
        ## Public message:
        logging.debug("SEND MESSAGE TO CLIENT: %s" % sdata)
        try: self.write_message(sdata)
        except: pass



    def on_close(self):
        logging.debug("CLOSING CLIENT: %s" % self)
        MessagesCommon.del_client(self)


    def finish(self, *args, **kwargs):
        try:
            MessagesCommon.del_client(self)
            logging.debug("CLOSING CLIENT: %s" % self)
        except Exception as err: 
            pass
        return super(messagesHandler, self).finish(*args, **kwargs)

