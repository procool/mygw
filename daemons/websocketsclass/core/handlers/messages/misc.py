import logging
import brukva
import json


class MessagesCommon(object):
    clients = []

    @classmethod
    def show_message(cls, data):
        logging.debug("NEW MESSAGE: %s" % data.body)
        mbody = str(data.body)
 
        try:   data_ = json.loads( mbody )
        except: return None

        if isinstance(data_, (list, tuple)):
            for msg in data_:
                cls._show_message(msg)
        else:
            cls._show_message(data_)

    @classmethod
    def _show_message(cls, data):
        data_raw = json.dumps(data)
        for client in cls.clients:
            client.show_new_message(data, data_raw)


    @classmethod
    def add_client(cls, client):
        cls.del_client(client)
        cls.clients.append(client)

    @classmethod
    def del_client(cls, client):
        cls.clients = [cl for cl in cls.clients if cl != client]



class redisChannels(object):
    hosts = []
    channels = {}
    new_message_callback = MessagesCommon.show_message

    avalible_channel_names = [
        'status_channel',
    ]

    @classmethod
    def get_hosts(cls_):
        cls_.hosts.append('localhost')

    @classmethod
    def set_channels(cls_):
        for host in cls_.hosts:
            cls_.set_channel(host)
 
    @classmethod
    def set_channel(cls_, host):
        cls_.channels[host] = []
        for channel in cls_.avalible_channel_names:
            cls_.channels[host].append( cls_.setup_channel(host, channel) )

    @classmethod
    def setup_channel(cls_, host, channel):
        c = brukva.Client(host=host, port=6379,)
        c.connect()
        c.subscribe(channel)
        c.listen(cls_.new_message_callback)
        return c





