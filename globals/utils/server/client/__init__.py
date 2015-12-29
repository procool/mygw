#!/usr/bin/env python

"""
client module for tcp server

Usage summary
=============

This should give you a feel for how this module operates::

    >>> import mytaxiclient
    >>> mc = mytaxiclient.Client(['127.0.0.1:9900'], debug=0)

    >>> ## Test server with echo command:
    >>> mc.echo()
    True


Detailed Documentation
======================

More detailed documentation is available in the L{Client} class.
"""

import logging
import sys
import socket
import time
import os
import re
import json

_DEAD_RETRY = 3  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 150  #  number of seconds before sockets timeout.



from binascii import crc32   # zlib version is not cross-platform
def cmytaxi_hash(key):
    return((((crc32(key) & 0xffffffff) >> 16) & 0x7fff) or 1)
serverHashFunction = cmytaxi_hash

try:
    from zlib import compress, decompress
    _supports_compress = True
except ImportError:
    _supports_compress = False
    # quickly define a decompress just in case we recv compressed data.
    def decompress(val):
        raise _Error("received compressed data but I don't support compression (import error)")


class _Error(Exception):
    pass


class _ConnectionDeadError(Exception):
    pass


"""
try:
    # Only exists in Python 2.4+
    from threading import local
except ImportError:
    # TODO:  add the pure-python local implementation
    class local(object):
        pass
"""

class local(object):
    pass

class AttributeInitType(type):
    def __call__(self, *args, **kwargs):
        obj = type.__call__(self, *args)
        for name in kwargs:
            setattr(obj, name, kwargs[name])
        setattr(obj, 'as_dict', kwargs)
        return obj


class CommandResult(object):
    __metaclass__ = AttributeInitType

def result_wrapper(func):
    def wrapped(*args, **kwargs):
        r = func(*args, **kwargs)
        if r is not None:
            r = CommandResult(**r)
        return r
    return wrapped

def test_for_result(func):
    def wrapped(*args, **kwargs):
        r = func(*args, **kwargs)
        if r is None:
            raise(Exception("No Answer!"))
        elif not hasattr(r, 'errno'):
            raise(Exception("Proto error!"))
        return r 
    return wrapped



class Client(local):

    _SERVER_RETRIES = 3  # how many times to try finding a free server.

    def __init__(self, servers, debug=0, pickleProtocol=0,
                 dead_retry=_DEAD_RETRY, socket_timeout=_SOCKET_TIMEOUT,
                 flush_on_reconnect=0,):

        local.__init__(self)


        self.debug = debug
        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout
        self.flush_on_reconnect = flush_on_reconnect
        self.set_servers(servers)
        self.stats = {}
        self.lastupdate = time.time()
        self.once_connected = False


    def set_servers(self, servers):
        """
        Set the pool of servers used by this client.

        @param servers: an array of servers.
        Servers can be passed in two forms:
            1. Strings of the form C{"host:port"}, which implies a default weight of 1.
            2. Tuples of the form C{("host:port", weight)}, where C{weight} is
            an integer weight value.
        """
        self.servers = [_Host(s, self.debug, dead_retry=self.dead_retry,
                socket_timeout=self.socket_timeout,
                flush_on_reconnect=self.flush_on_reconnect)
                    for s in servers]
        self._init_buckets()




    def get_stats(self, stat_args = None):
        '''Get statistics from each of the servers.

        @param stat_args: Additional arguments to pass to the mytaxi
            "stats" command.

        @return: A list of tuples ( server_identifier, stats_dictionary ).
            The dictionary contains a number of name/value pairs specifying
            the name of the status field and the string value associated with
            it.  The values are not converted from strings.
        '''
        data = []
        for s in self.servers:
            if not s.connect(): continue
            if s.family == socket.AF_INET6:
                name = '[%s]:%s (%s)' % ( s.ip, s.port, s.weight )
            else:
                name = '%s:%s (%s)' % ( s.ip, s.port, s.weight )
            if not stat_args:
                s.send_cmd('stats')
            else:
                s.send_cmd('stats ' + stat_args)
            serverData = {}
            data.append(( name, serverData ))
            readline = s.readline
            while 1:
                line = readline()
                if not line or line.strip() == 'END': break
                stats = line.split(' ', 2)
                serverData[stats[1]] = stats[2]

        return(data)

    def flush_all(self):
        """Expire all data in myTaxi servers that are reachable."""
        for s in self.servers:
            if not s.connect(): continue
            s.flush()



    def debuglog(self, str):
        if self.debug:
            sys.stderr.write("myTaxi: %s\n" % str)


    def _statlog(self, func):
        if func not in self.stats:
            self.stats[func] = 1
        else:
            self.stats[func] += 1


    def forget_dead_hosts(self):
        """
        Reset every host in the pool to an "alive" state.
        """
        for s in self.servers:
            s.deaduntil = 0

    def _init_buckets(self):
        self.buckets = []
        for server in self.servers:
            for i in range(server.weight):
                self.buckets.append(server)



    def _get_server(self, key):
        if isinstance(key, tuple):
            serverhash, key = key
        else:
            serverhash = serverHashFunction(key)

        if not self.buckets:
            return None, None

        for i in range(Client._SERVER_RETRIES):
            server = self.buckets[serverhash % len(self.buckets)]
            if server.connect():
                self.once_connected += 1
                return server, key
            serverhash = serverHashFunction(str(serverhash) + str(i))
        return None, None

    def disconnect_all(self):
        for s in self.servers:
            s.close_socket()



    def echo(self):
        '''Push echo command to server.

        @return: True on success.
        @rtype: boolean
        '''
        res = self.exec_command('echo', test_data=123)
            
        if res is not None and \
           hasattr(res, 'cmd') and res.cmd == 'echo' and \
           hasattr(res, 'test_data') and res.test_data == 123:
            return True
        return False



    @test_for_result
    def quit(self, **kwargs):
        return self.exec_command('quit', **kwargs)




    @result_wrapper
    def exec_command(self, *args, **kwargs):
        err_ = None
        for i in xrange(3):
            try: return self._exec_command(*args, **kwargs)
            except Exception as err: 
                err_ = err
            time.sleep(1)
        raise(err_)
        

    def _exec_command(self, cmd, retrys=0, **to_send):

        cmd_ = { 'cmd' : cmd }
        to_send.update(cmd_)

        to_send_ = json.dumps(to_send)

        server, cmd = self._get_server(cmd)
        if not server:
            return None
        self._statlog(cmd)

        try:
            server.send_cmd(to_send_)
            line = server.readline()
        except socket.error, msg:
            if isinstance(msg, tuple): msg = msg[1]
            #server.mark_dead(msg)
            server.close_socket()
            if retrys >= 0 or not server.connect():
            	return None
            else:
                retrys += 1
                server.deaduntil = 0
                try: s = to_send.pop('cmd')
                except: pass
                print "FFFFFFFFFF", retrys
                return self.exec_command(cmd, retrys=retrys, **to_send)

        try:
            r = json.loads(line)
        except:
            return None
        self.lastupdate = time.time()
        
        return r

    @property
    def update_timeout(self):
        return time.time() - self.lastupdate

class _Host(object):

    def __init__(self, host, debug=0, dead_retry=_DEAD_RETRY, 
                 socket_timeout=_SOCKET_TIMEOUT, flush_on_reconnect=0):

        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout
        self.debug = debug
        self.flush_on_reconnect = flush_on_reconnect

        if isinstance(host, tuple):
            host, self.weight = host
        else:
            self.weight = 1


        #  parse the connection string
        m = re.match(r'^(?P<proto>inet6):'
                     r'\[(?P<host>[^\[\]]+)\](:(?P<port>[0-9]+))?$', host)
        if not m:
            m = re.match(r'^(?P<proto>inet):'
                    r'(?P<host>[^:]+)(:(?P<port>[0-9]+))?$', host)
        if not m: m = re.match(r'^(?P<host>[^:]+)(:(?P<port>[0-9]+))?$', host)
        if not m:
            raise ValueError('Unable to parse connection string: "%s"' % host)

        hostData = m.groupdict()
        if hostData.get('proto') == 'inet6':
            self.family = socket.AF_INET6
            self.ip = hostData['host']
            self.port = int(hostData.get('port') or 9900)
            self.address = ( self.ip, self.port )
        else:
            self.family = socket.AF_INET
            self.ip = hostData['host']
            self.port = int(hostData.get('port') or 9900)
            self.address = ( self.ip, self.port )


        self.deaduntil = 0
        self.socket = None
        self.flush_on_next_connect = 0

        self.buffer = ''


    def debuglog(self, str):
        if self.debug:
            sys.stderr.write("myTaxi: %s\n" % str)

    def _check_dead(self):
        if self.deaduntil and self.deaduntil > time.time():
            return 1
        self.deaduntil = 0
        return 0


    def connect(self):
        if self._get_socket():
            return 1
        return 0


    def mark_dead(self, reason):
        self.debuglog("%s: %s.  Marking dead." % (self, reason))
        self.deaduntil = time.time() + self.dead_retry
        if self.flush_on_reconnect:
            self.flush_on_next_connect = 1
        self.close_socket()


    def _get_socket(self):
        if self._check_dead():
            return None
        if self.socket:
            return self.socket
        s = socket.socket(self.family, socket.SOCK_STREAM)
        if hasattr(s, 'settimeout'): s.settimeout(self.socket_timeout)
        try:
            s.connect(self.address)
        except socket.timeout, msg:
            self.mark_dead("connect: %s" % msg)
            return None
        except socket.error, msg:
            if isinstance(msg, tuple): msg = msg[1]
            self.mark_dead("connect: %s" % msg[1])
            return None
        self.socket = s
        self.buffer = ''
        if self.flush_on_next_connect:
            self.flush()
            self.flush_on_next_connect = 0
        return s



    def close_socket(self):
        if self.socket:
            logging.debug("TCP Client: Closing socket: %s" % self.socket)
            self.socket.close()
            self.socket = None

    def send_cmd(self, cmd):
        self.socket.sendall(cmd + '\r\n')

    def send_cmds(self, cmds):
        """ cmds already has trailing \r\n's applied """
        self.socket.sendall(cmds)




    def readline(self, raise_exception=False):
        """Read a line and return it.  If "raise_exception" is set,
        raise _ConnectionDeadError if the read fails, otherwise return
        an empty string.
        """
        buf = self.buffer
        if self.socket:
            recv = self.socket.recv
        else:
            recv = lambda bufsize: ''

        while True:
            index = buf.find('\r\n')
            if index >= 0:
                break
            data = recv(4096)
            if not data:
                # connection close, let's kill it and raise
                self.mark_dead('connection closed in readline()')
                if raise_exception:
                    raise _ConnectionDeadError()
                else:
                    return ''

            buf += data
        self.buffer = buf[index+2:]
        return buf[:index]

    def expect(self, text, raise_exception=False):
        line = self.readline(raise_exception)
        if line != text:
            self.debuglog("while expecting '%s', got unexpected response '%s'"
                    % (text, line))
        return line

    def recv(self, rlen):
        self_socket_recv = self.socket.recv
        buf = self.buffer
        while len(buf) < rlen:
            foo = self_socket_recv(max(rlen - len(buf), 4096))
            buf += foo
            if not foo:
                raise _Error( 'Read %d bytes, expecting %d, '
                        'read returned 0 length bytes' % ( len(buf), rlen ))
        self.buffer = buf[rlen:]
        return buf[:rlen]

    def flush(self):
        self.send_cmd('flush_all')
        self.expect('OK')




    def __str__(self):
        d = ''
        if self.deaduntil:
            d = " (dead until %d)" % self.deaduntil

        if self.family == socket.AF_INET6:
            return "inet6:[%s]:%d%s" % (self.address[0], self.address[1], d)
        elif self.family == socket.AF_INET:
            return "inet:%s:%d%s" % (self.address[0], self.address[1], d)

        return "inet:%s%s" % (self.address, d)




