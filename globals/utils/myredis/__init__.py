# -*- coding: utf-8 -*-

import json
import redis
import logging
import gevent

class Message(dict):

    def __init__(self, message=None, **kwargs):

        if message is not None:
            self.message = message

        has_slots = False
        if hasattr(self, '__slots__'):
            has_slots = True

        for attr in kwargs:
            if has_slots and attr not in self.__slots__:
                continue
            setattr(self, attr, kwargs[attr])
            self[attr] = kwargs[attr]

        ## If slots, set None for any used attr as default:
        if has_slots:
            for attr in self.__slots__:
                if not hasattr(self, attr):
                    setattr(self, attr, None)
                    self[attr] = None




class myRedis(object):

    known_instances = {}
            
    def __new__(cls, *args, **kwargs):
        try:
            inst = kwargs.pop('instance')
            try:
                instance = cls.known_instances[inst]
            except Exception as err:
                instance = super(myRedis, cls).__new__(cls)
                cls.known_instances[inst] = instance
                instance.__init(*args, **kwargs)
                
        except Exception as err:  
            instance = super(myRedis, cls).__new__(cls)
            instance.__init(*args, **kwargs)

        return instance


    def __init(self, channel=None, incoming=None, use_gevent=True, **kwargs):
        self.is_exit  = False
        self.use_gevent  = use_gevent
        self.channel  = channel
        self.incoming = incoming
        self.pack = []

        ## Connect to Redis:
        self.c = redis.Redis(**kwargs)


    def stop(self):
        self.is_exit = True
        ##self.cp.unsubscribe()
        self.cp.close()


    def start(self):
        if self.incoming is None:
            return

        if not self.use_gevent:
            raise Exception('Can not listen without gevents!')

        self.cp = self.c.pubsub()
        if self.channel is not None:
            self.cp.subscribe(self.channel)

        gevent.spawn(self.run)


    def run(self):
        """Listens for new messages in Redis"""
        for data in self.__iter_data():
            if not data: continue

            ## A pack of messages:
            if type(data) is list:
                for line in data:
                    gevent.spawn(self._incoming, line)

            ## Single message:
            else:
                gevent.spawn(self._incoming, data)


    def __iter_data(self):
        for m in self.cp.listen():
            data = None
            try:    data = json.loads( m.get('data') )
            except: yield None
            yield data



    def _incoming(self, data):
        logging.debug("REDIS: INCOMMING: %s" % data)
        self.incoming(data)


    ## Send messages to Redis:
    ## !!! 'message' arg should be a Message instance !!!
    def sendpack(self, message=None, flush=False, **kwargs):
        if message is not None:
            self.pack.append(message)

        if flush and len(self.pack)>0:
            if self.use_gevent:
                gevent.spawn(self._send, from_pack=True, **kwargs)
            else:
                self._send(from_pack=True, **kwargs)


    ## Send message to Redis:
    def send(self, message, **kwargs):
        msg = message
        if self.use_gevent:
            gevent.spawn(self._send, msg, **kwargs)
        else:
            self._send(msg, **kwargs)




    def _send(self, message={}, from_pack=False, channel=None, **kwargs):

        if not channel:
            channel = self.channel

        if from_pack:
            message, self.pack = self.pack, []

        logging.debug("REDIS: SENDMESSAGE(from pack=%s): %s" % (from_pack, message))
        self.c.publish(channel, json.dumps(message))


