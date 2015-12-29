import logging
import time
import socket

LOGGING_PREFIX = "TCP CONNECTOR: "
DEAD_RETRY = 0.5       ## Retry time in seconds
SOCKET_TIMEOUT = 15
DEBUG=False

class Connector(object):

    def __init__(self, host, port, dead_retry=DEAD_RETRY, 
                 socket_timeout=SOCKET_TIMEOUT, proto=None, 
                 weight=1, on_connect=None, do_reconnect=False):

        self.host = host
        self.port = port
        self.weight = weight
        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout
        self.family = socket.AF_INET
        self.on_connect = on_connect
        self.do_reconnect = do_reconnect

        if proto == 'inet6':
            self.family = socket.AF_INET6

        self.address = ( self.host, self.port )

        self.deaduntil = 0
        self.__socket = None

        self.buffer = ''



    @property
    def is_connected(self):
        if self.is_dead:
            return False
        if self.socket is None:
            return False
        return True 


    def mark_dead(self, reason):
        if self.is_dead:
            return True
        logging.info(LOGGING_PREFIX + "%s:%s: %s.  Marking dead." % (self.host, self.port, reason))
        if self.do_reconnect:
            self.deaduntil = time.time() + self.dead_retry
        else:
            self.deaduntil = -1
        self.close()


    @property
    def is_dead(self):
        if self.deaduntil > 0 and self.deaduntil > time.time():
            return True
        if self.deaduntil < 0:
            return True
        return False


    def connect(self):
        return self.socket
        

    @property
    def socket(self):
        if self.is_dead:
            return None
        if self.__socket is not None:
            return self.__socket

        ## Connect to server:
        if DEBUG:
            logging.debug(LOGGING_PREFIX + "Making connection to: %s:%s" % (self.host, self.port))
        s = socket.socket(self.family, socket.SOCK_STREAM)
        if hasattr(s, 'settimeout'): s.settimeout(self.socket_timeout)
        try:
            s.connect(self.address)
        except socket.timeout, msg:
            self.mark_dead("connect: %s" % msg)
            return None
        except socket.error, msg:
            if isinstance(msg, tuple): 
                msg = msg[1]
            self.mark_dead("connect: %s" % msg[1])
            return None
        self.__socket = s
        self.buffer = ''
        if self.on_connect is not None:
            self.on_connect()
        return s


            
    def disconnect(self):
        self.close()

    def close(self):
        if self.__socket is None:
            return None
        if DEBUG:
            logging.debug(LOGGING_PREFIX + "Closing socket: %s" % self.__socket)
        self.__socket.close()
        self.__socket = None
        return True



    def readline(self, raise_exception=False):
        """Read a line and return it.  If "raise_exception" is set,
        raise _ConnectionDeadError if the read fails, otherwise return
        an empty string.
        """
        buf = self.buffer
        if self.is_connected:
            recv = self.__socket.recv
        else:
            recv = lambda bufsize: ''

        while True:
            index = buf.find('\r\n')
            if index >= 0:
                break
            try: data = recv(4096)
            except: data = ''
            if not data:
                # connection close, let's kill it and raise
                #if self.is_connected:
                #    self.mark_dead('connection closed in readline()')
                #elif not self.is_dead:
                #    self.connect()
                if raise_exception:
                    raise Exception("connection terminated!")
                else:
                    return ''
        
            buf += data
        self.buffer = buf[index+2:]
        return buf[:index]

        
    def send_cmd(self, cmd):
        return self.send(cmd + '\r\n')
            
    def send(self, data):
        if self.socket is None:
            return False

        """ data already has trailing \r\n's applied """
        ##return self.socket.sendall(data)
        self.socket.sendall(data)
        return True




