#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
from datetime import datetime
import traceback as tb
import time

from tornado.ioloop import IOLoop

import brukva
from brukva.adisp import process, async
from brukva.exceptions import ResponseError, RequestError

import logging; logging.basicConfig()
def callable(obj):
    return hasattr(obj, '__call__')

class CustomAssertionError(AssertionError):
    io_loop = None

    def __init__(self, *args, **kwargs):
        super(CustomAssertionError, self).__init__(*args, **kwargs)
        CustomAssertionError.io_loop.stop()

def handle_callback_exception(callback):
    (type, value, traceback) = sys.exc_info()
    raise type, value, None

class TornadoTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TornadoTestCase, self).__init__(*args, **kwargs)
        self.failureException = CustomAssertionError

    def setUp(self):
        self.loop = IOLoop.instance()
        setattr(self.loop, 'handle_callback_exception', handle_callback_exception)
        CustomAssertionError.io_loop = self.loop
        self.client = brukva.Client(io_loop=self.loop)
        self.client.connection.connect()
        self.client.select(9)
        self.client.flushdb()

    def tearDown(self):
        del self.client

    def expect(self, expected):
        source_line = '\n' + tb.format_stack()[-2]
        def callback(result):
            if isinstance(expected, Exception):
                self.assertTrue(isinstance(result, expected),
                    msg=source_line+'  Got:'+repr(result))
            if callable(expected):
                self.assertTrue(expected(result),
                    msg=source_line+'  Got:'+repr(result))
            else:
                self.assertEqual(expected, result,
                    msg=source_line+'  Got:'+repr(result))
        callback.__name__ = "expect_%s" % repr(expected)
        return callback

    def pexpect(self, expected_list, list_without_errors=True):
        if list_without_errors:
            expected_list = [(None, el) for el in expected_list]

        source_line = '\n' + tb.format_stack()[-2]
        def callback(result):
            if isinstance(result, Exception):
                self.fail('got exception %s' % result)

            self.assertEqual(len(result), len(expected_list) )
            for result, (exp_e, exp_d)  in zip(result, expected_list):
                if exp_e:
                    self.assertTrue( isinstance(result, exp_e),
                        msg=source_line+'  Error:'+repr(result))
                elif callable(exp_d):
                    self.assertTrue(exp_d(result),
                        msg=source_line+'  Got:'+repr(result))
                else:
                    self.assertEqual(result, exp_d,
                        msg=source_line+'  Got:'+repr(result))
        return callback

    def delayed(self, timeout, cb):
        self.loop.add_timeout(time.time()+timeout, cb)

    def finish(self, *args, **kwargs):
        self.loop.stop()

    def start(self):
        self.loop.start()


class ServerCommandsTestCase(TornadoTestCase):
    def test_setget_unicode(self):
        self.client.set('foo', u'бар', self.expect(True))
        self.client.get('foo', [self.expect('бар'), self.finish])
        self.start()

    def test_set(self):
        self.client.set('foo', 'bar', [self.expect(True), self.finish])
        self.start()

    def test_setex(self):
        self.client.setex('foo', 5, 'bar', self.expect(True))
        self.client.ttl('foo', [self.expect(5), self.finish])
        self.start()

    def test_setnx(self):
        self.client.setnx('a', 1, self.expect(True))
        self.client.setnx('a', 0, [self.expect(False), self.finish])
        self.start()

    def test_get(self):
        self.client.set('foo', 'bar', self.expect(True))
        self.client.get('foo', [self.expect('bar'), self.finish])
        self.start()

    def test_randomkey(self):
        self.client.set('a', 1, self.expect(True))
        self.client.set('b', 1, self.expect(True))
        self.client.randomkey(self.expect(lambda k: k in ['a', 'b']))
        self.client.randomkey(self.expect(lambda k: k in ['a', 'b']))
        self.client.randomkey([self.expect(lambda k: k in ['a', 'b']), self.finish])
        self.start()

    def test_substr(self):
        self.client.set('foo', 'lorem ipsum', self.expect(True))
        self.client.substr('foo', 2, 4, [self.expect('rem'), self.finish])
        self.start()

    def test_append(self):
        self.client.set('foo', 'lorem ipsum', self.expect(True))
        self.client.append('foo', ' bar', self.expect(15))
        self.client.get('foo', [self.expect('lorem ipsum bar'), self.finish])
        self.start()

    def test_dbsize(self):
        self.client.set('a', 1, self.expect(True))
        self.client.set('b', 2, self.expect(True))
        self.client.dbsize([self.expect(2), self.finish])
        self.start()

    def test_save(self):
        self.client.save(self.expect(True))
        now = datetime.now().replace(microsecond=0)
        self.client.lastsave([self.expect(lambda d: d >= now), self.finish])
        self.start()

    def test_keys(self):
        self.client.set('a', 1, self.expect(True))
        self.client.set('b', 2, self.expect(True))
        self.client.keys('*', self.expect(['a', 'b']))
        self.client.keys('', self.expect([]))

        self.client.set('foo_a', 1, self.expect(True))
        self.client.set('foo_b', 2, self.expect(True))
        self.client.keys('foo_*', [self.expect(['foo_a', 'foo_b']), self.finish])
        self.start()

    def test_expire(self):
        self.client.set('a', 1, self.expect(True))
        self.client.expire('a', 10, self.expect(True))
        self.client.ttl('a', [self.expect(10), self.finish])
        self.start()

    def test_type(self):
        self.client.set('a', 1, self.expect(True))
        self.client.type('a', self.expect('string'))
        self.client.rpush('b', 1, self.expect(True))
        self.client.type('b', self.expect('list'))
        self.client.sadd('c', 1, self.expect(True))
        self.client.type('c', self.expect('set'))
        self.client.hset('d', 'a', 1, self.expect(True))
        self.client.type('d', self.expect('hash'))
        self.client.zadd('e', 1, 1, self.expect(True))
        self.client.type('e', [self.expect('zset'), self.finish])
        self.start()

    def test_rename(self):
        self.client.set('a', 1, self.expect(True))
        self.client.rename('a', 'b', self.expect(True))
        self.client.set('c', 1, self.expect(True))
        self.client.renamenx('c', 'b', [self.expect(False), self.finish])
        self.start()

    def test_move(self):
        self.client.select(8, self.expect(True))
        self.client.delete('a', self.expect(True))
        self.client.select(9, self.expect(True))
        self.client.set('a', 1, self.expect(True))
        self.client.move('a', 8, self.expect(True))
        self.client.exists('a', self.expect(False))
        self.client.select(8, self.expect(True))
        self.client.get('a', [self.expect('1'), self.finish])
        self.start()

    def test_exists(self):
        self.client.set('a', 1, self.expect(True))
        self.client.exists('a', self.expect(True))
        self.client.delete('a', self.expect(True))
        self.client.exists('a', [self.expect(False), self.finish])
        self.start()

    def test_mset_mget(self):
        self.client.mset({'a': 1, 'b': 2}, self.expect(True))
        self.client.get('a', self.expect('1'))
        self.client.get('b', self.expect('2'))
        self.client.mget(['a', 'b'], [self.expect(['1', '2']), self.finish])
        self.start()

    def test_msetnx(self):
        self.client.msetnx({'a': 1, 'b': 2}, self.expect(True))
        self.client.msetnx({'b': 3, 'c': 4}, [self.expect(False), self.finish])
        self.start()

    def test_getset(self):
        self.client.set('a', 1, self.expect(True))
        self.client.getset('a', 2, self.expect('1'))
        self.client.get('a', [self.expect('2'), self.finish])
        self.start()

    def test_hash(self):
        self.client.hmset('foo', {'a': 1, 'b': 2}, self.expect(True))
        self.client.hgetall('foo', self.expect({'a': '1', 'b': '2'}))
        self.client.hdel('foo', 'a', self.expect(True))
        self.client.hgetall('foo', self.expect({'b': '2'}))
        self.client.hget('foo', 'a', self.expect(''))
        self.client.hget('foo', 'b', self.expect('2'))
        self.client.hlen('foo', self.expect(1))
        self.client.hincrby('foo', 'b', 3, self.expect(5))
        self.client.hkeys('foo', self.expect(['b']))
        self.client.hvals('foo', self.expect(['5']))
        self.client.hset('foo', 'a', 1, self.expect(True))
        self.client.hmget('foo', ['a', 'b'], self.expect({'a': '1', 'b': '5'}))
        self.client.hexists('foo', 'b', [self.expect(True), self.finish])
        self.start()

    def test_incrdecr(self):
        self.client.incr('foo', self.expect(1))
        self.client.incrby('foo', 10, self.expect(11))
        self.client.decr('foo', self.expect(10))
        self.client.decrby('foo', 10, self.expect(0))
        self.client.decr('foo', [self.expect(-1), self.finish])
        self.start()

    def test_ping(self):
        self.client.ping([self.expect(True), self.finish])
        self.start()

    def test_lists(self):
        self.client.lpush('foo', 1, self.expect(True))
        self.client.llen('foo', self.expect(1))
        self.client.lrange('foo', 0, -1, self.expect(['1']))
        self.client.rpop('foo', self.expect('1'))
        self.client.llen('foo', [self.expect(0), self.finish])
        self.start()

    def test_brpop(self):
        self.client.lpush('foo', 'ab', self.expect(True))
        self.client.lpush('bar', 'cd', self.expect(True))
        self.client.brpop(['foo', 'bar'], 1, self.expect({'foo':'ab'}))
        self.client.llen('foo', self.expect(0))
        self.client.llen('bar', self.expect(1))
        self.client.brpop(['foo', 'bar'], 1, [self.expect({'bar':'cd'}), self.finish])
        self.start()

    def test_brpoplpush(self):
        self.client.lpush('foo', 'ab', self.expect(True))
        self.client.lpush('bar', 'cd', self.expect(True))
        self.client.lrange('foo', 0, -1, self.expect(['ab']))
        self.client.lrange('bar', 0, -1, self.expect(['cd']))
        self.client.brpoplpush('foo', 'bar', callbacks=[self.expect('ab'), self.finish])
        self.client.llen('foo', self.expect(0))
        self.client.lrange('bar', 0, -1, [self.expect(['ab', 'cd']), self.finish])
        self.start()

    def test_sets(self):
        self.client.smembers('foo', self.expect(set()))
        self.client.sadd('foo', 'a', self.expect(1))
        self.client.sadd('foo', 'b', self.expect(1))
        self.client.sadd('foo', 'c', self.expect(1))
        self.client.srandmember('foo', self.expect(lambda x: x in ['a', 'b', 'c']))
        self.client.scard('foo', self.expect(3))
        self.client.srem('foo', 'a', self.expect(True))
        self.client.smove('foo', 'bar', 'b', self.expect(True))
        self.client.smembers('bar', self.expect(set(['b'])))
        self.client.sismember('foo', 'c', self.expect(True))
        self.client.spop('foo', [self.expect('c'), self.finish])
        self.start()

    def test_sets2(self):
        self.client.sadd('foo', 'a', self.expect(1))
        self.client.sadd('foo', 'b', self.expect(1))
        self.client.sadd('foo', 'c', self.expect(1))
        self.client.sadd('bar', 'b', self.expect(1))
        self.client.sadd('bar', 'c', self.expect(1))
        self.client.sadd('bar', 'd', self.expect(1))

        self.client.sdiff(['foo', 'bar'], self.expect(set(['a'])))
        self.client.sdiff(['bar', 'foo'], self.expect(set(['d'])))
        self.client.sinter(['foo', 'bar'], self.expect(set(['b', 'c'])))
        self.client.sunion(['foo', 'bar'], [self.expect(set(['a', 'b', 'c', 'd'])), self.finish])
        self.start()

    def test_sets3(self):
        self.client.sadd('foo', 'a', self.expect(1))
        self.client.sadd('foo', 'b', self.expect(1))
        self.client.sadd('foo', 'c', self.expect(1))
        self.client.sadd('bar', 'b', self.expect(1))
        self.client.sadd('bar', 'c', self.expect(1))
        self.client.sadd('bar', 'd', self.expect(1))

        self.client.sdiffstore(['foo', 'bar'], 'zar', self.expect(1))
        self.client.smembers('zar', self.expect(set(['a'])))
        self.client.delete('zar', self.expect(True))

        self.client.sinterstore(['foo', 'bar'], 'zar', self.expect(2))
        self.client.smembers('zar', self.expect(set(['b', 'c'])))
        self.client.delete('zar', self.expect(True))

        self.client.sunionstore(['foo', 'bar'], 'zar', self.expect(4))
        self.client.smembers('zar', [self.expect(set(['a', 'b', 'c', 'd'])), self.finish])
        self.start()

    def test_zsets(self):
        self.client.zadd('foo', 1, 'a', self.expect(1))
        self.client.zadd('foo', 2, 'b', self.expect(1))
        self.client.zscore('foo', 'a', self.expect(1))
        self.client.zscore('foo', 'b', self.expect(2))
        self.client.zrank('foo', 'a', self.expect(0))
        self.client.zrank('foo', 'b', self.expect(1))
        self.client.zrevrank('foo', 'a', self.expect(1))
        self.client.zrevrank('foo', 'b', self.expect(0))
        self.client.zincrby('foo', 'a', 1, self.expect(2))
        self.client.zincrby('foo', 'b', 1, self.expect(3))
        self.client.zscore('foo', 'a', self.expect(2))
        self.client.zscore('foo', 'b', self.expect(3))
        self.client.zrange('foo', 0, -1, True, self.expect([('a', 2.0), ('b', 3.0)]))
        self.client.zrange('foo', 0, -1, False, self.expect(['a', 'b']))
        self.client.zrevrange('foo', 0, -1, True, self.expect([('b', 3.0), ('a', 2.0)]))
        self.client.zrevrange('foo', 0, -1, False, self.expect(['b', 'a']))
        self.client.zcard('foo', [self.expect(2)])
        self.client.zadd('foo', 3.5, 'c', self.expect(1))
        self.client.zrangebyscore('foo', '-inf', '+inf', None, None, False, self.expect(['a', 'b', 'c']))
        self.client.zrangebyscore('foo', '2.1', '+inf', None, None, True, self.expect([('b', 3.0), ('c', 3.5)]))
        self.client.zrangebyscore('foo', '-inf', '3.0', 0, 1, False, self.expect(['a']))
        self.client.zrangebyscore('foo', '-inf', '+inf', 1, 2, False, self.expect(['b', 'c']))

        self.client.delete('foo', self.expect(True))
        self.client.zadd('foo', 1, 'a', self.expect(1))
        self.client.zadd('foo', 2, 'b', self.expect(1))
        self.client.zadd('foo', 3, 'c', self.expect(1))
        self.client.zadd('foo', 4, 'd', self.expect(1))
        self.client.zremrangebyrank('foo', 2, 4, self.expect(2))
        self.client.zremrangebyscore('foo', 0, 2, [self.expect(2), self.finish()])

        self.client.zadd('a', 1, 'a1', self.expect(1))
        self.client.zadd('a', 1, 'a2', self.expect(1))
        self.client.zadd('a', 1, 'a3', self.expect(1))
        self.client.zadd('b', 2, 'a1', self.expect(1))
        self.client.zadd('b', 2, 'a3', self.expect(1))
        self.client.zadd('b', 2, 'a4', self.expect(1))
        self.client.zadd('c', 6, 'a1', self.expect(1))
        self.client.zadd('c', 5, 'a3', self.expect(1))
        self.client.zadd('c', 4, 'a4', self.expect(1))

        # ZINTERSTORE
        # sum, no weight
        self.client.zinterstore('z', ['a', 'b', 'c'], callbacks=self.expect(2))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=self.expect([('a3', 8),
                                                                                ('a1', 9),
                                                                                ]))
        # max, no weight
        self.client.zinterstore('z', ['a', 'b', 'c'], aggregate='MAX', callbacks=self.expect(2))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=self.expect([('a3', 5),
                                                                                ('a1', 6),
                                                                                ]))
        # with weight
        self.client.zinterstore('z', {'a': 1, 'b': 2, 'c': 3}, callbacks=self.expect(2))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=[self.expect([('a3', 20),
                                                                                 ('a1', 23),
                                                                                 ]),
                                                                    self.finish()])

        # ZUNIONSTORE
        # sum, no weight
        self.client.zunionstore('z', ['a', 'b', 'c'], callbacks=self.expect(5))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=self.expect([('a2', 1),
                                                                                ('a3', 3),
                                                                                ('a5', 4),
                                                                                ('a4', 7),
                                                                                ('a1', 9),
                                                                                ]))
        # max, no weight
        self.client.zunionstore('z', ['a', 'b', 'c'], aggregate='MAX', callbacks=self.expect(5))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=self.expect([('a2', 1),
                                                                                ('a3', 2),
                                                                                ('a5', 4),
                                                                                ('a4', 5),
                                                                                ('a1', 6),
                                                                                ]))
        # with weight
        self.client.zunionstore('z', {'a': 1, 'b': 2, 'c': 3}, callbacks=self.expect(5))
        self.client.zrange('z', 0, -1, with_scores=True, callbacks=[self.expect([('a2', 1),
                                                                                 ('a3', 5),
                                                                                 ('a5', 12),
                                                                                 ('a4', 19),
                                                                                 ('a1', 23),
                                                                                 ]),
                                                                    self.finish,
                                                                    ])
        self.start()

    def test_long_zset(self):
        NUM = 1000
        long_list = map(str, xrange(0, NUM))
        for i in long_list:
            self.client.zadd('foobar', i, i, self.expect(1))
        self.client.zrange('foobar', 0, NUM, with_scores=False, callbacks=[self.expect(long_list),  self.finish])
        self.start()

    def test_sort(self):
        def make_list(key, items, expect_value=True):
            self.client.delete(key, callbacks=self.expect(expect_value))
            for i in items:
                self.client.rpush(key, i)
        self.client.sort('a', callbacks=self.expect([]))
        make_list('a', '3214', False)
        self.client.sort('a', callbacks=self.expect(['1', '2', '3', '4']))
        self.client.sort('a', start=1, num=2, callbacks=self.expect(['2', '3']))

        self.client.set('score:1', 8, callbacks=self.expect(True))
        self.client.set('score:2', 3, callbacks=self.expect(True))
        self.client.set('score:3', 5, callbacks=self.expect(True))
        make_list('a_values', '123')
        self.client.sort('a_values', by='score:*', callbacks=self.expect(['2', '3', '1']))

        self.client.set('user:1', 'u1', callbacks=self.expect(True))
        self.client.set('user:2', 'u2', callbacks=self.expect(True))
        self.client.set('user:3', 'u3', callbacks=self.expect(True))

        make_list('a', '231')
        self.client.sort('a', get='user:*', callbacks=self.expect(['u1', 'u2', 'u3']))

        make_list('a', '231')
        self.client.sort('a', desc=True, callbacks=self.expect(['3', '2', '1']))

        make_list('a', 'ecdba')
        self.client.sort('a', alpha=True, callbacks=self.expect(['a', 'b', 'c', 'd', 'e']))

        make_list('a', '231')
        self.client.sort('a', store='sorted_values', callbacks=self.expect(3))
        self.client.lrange('a', 0, -1, callbacks=self.expect(['1', '2', '3']))

        self.client.set('user:1:username', 'zeus')
        self.client.set('user:2:username', 'titan')
        self.client.set('user:3:username', 'hermes')
        self.client.set('user:4:username', 'hercules')
        self.client.set('user:5:username', 'apollo')
        self.client.set('user:6:username', 'athena')
        self.client.set('user:7:username', 'hades')
        self.client.set('user:8:username', 'dionysus')
        self.client.set('user:1:favorite_drink', 'yuengling')
        self.client.set('user:2:favorite_drink', 'rum')
        self.client.set('user:3:favorite_drink', 'vodka')
        self.client.set('user:4:favorite_drink', 'milk')
        self.client.set('user:5:favorite_drink', 'pinot noir')
        self.client.set('user:6:favorite_drink', 'water')
        self.client.set('user:7:favorite_drink', 'gin')
        self.client.set('user:8:favorite_drink', 'apple juice')
        make_list('gods', '12345678')
        self.client.sort('gods',
                         start=2,
                         num=4,
                         by='user:*:username',
                         get='user:*:favorite_drink',
                         desc=True,
                         alpha=True,
                         store='sorted',
                         callbacks=self.expect(4))
        self.client.lrange('sorted', 0, -1, callbacks=[self.expect(['vodka',
                                                                    'milk',
                                                                    'gin',
                                                                    'apple juice',
                                                                    ]),
                                                       self.finish()])
        self.start()



class PipelineTestCase(TornadoTestCase):
    ### Pipeline ###
    def test_pipe_simple(self):
        pipe = self.client.pipeline()
        pipe.set('foo', '123')
        pipe.set('bar', '456')
        pipe.mget( ('foo', 'bar') )

        pipe.execute([self.pexpect([True , True, ['123', '456',]]), self.finish])
        self.start()

    def test_pipe_multi(self):
        pipe = self.client.pipeline(transactional=True)
        pipe.set('foo', '123')
        pipe.set('bar', '456')
        pipe.mget( ('foo', 'bar') )

        pipe.execute([self.pexpect([True , True, ['123', '456',]]), self.finish])
        self.start()

    def test_pipe_error(self):
        pipe = self.client.pipeline()
        pipe.sadd('foo', 1)
        pipe.sadd('foo', 2)
        pipe.rpop('foo')

        pipe.execute([self.pexpect([(None, True), (None, True), (ResponseError, None)], False), self.finish])
        self.start()

    def test_two_pipes(self):
        pipe = self.client.pipeline()

        pipe.rpush('foo', '1')
        pipe.rpush('foo', '2')
        pipe.lrange('foo', 0, -1)
        pipe.execute([self.pexpect([True, 2, ['1', '2']]) ] )

        pipe.sadd('bar', '3')
        pipe.sadd('bar', '4')
        pipe.smembers('bar')
        pipe.scard('bar')
        pipe.execute([self.pexpect([1, 1, set(['3', '4']), 2]), self.finish])

        self.start()

    def test_mix_with_pipe(self):
        pipe = self.client.pipeline()

        self.client.set('foo', '123', self.expect(True))
        self.client.hmset('bar', {'zar': 'gza'},)

        pipe.get('foo')
        self.client.get('foo', self.expect('123') )

        pipe.hgetall('bar')

        pipe.execute([self.pexpect(['123', {'zar': 'gza'}]), self.finish])
        self.start()


    def test_mix_with_pipe_multi(self):
        pipe = self.client.pipeline(transactional=True)

        self.client.set('foo', '123', self.expect(True))
        self.client.hmset('bar', {'zar': 'gza'},)

        pipe.get('foo')
        self.client.get('foo', self.expect('123') )

        pipe.hgetall('bar')

        pipe.execute([self.pexpect(['123', {'zar': 'gza'}]), self.finish])
        self.start()

    def test_pipe_watch(self):
        self.client.watch('foo', self.expect(True))
        self.client.set('bar', 'zar', self.expect(True))
        pipe = self.client.pipeline(transactional=True)
        pipe.get('bar')
        pipe.execute([self.pexpect(['zar',]), self.finish])
        self.start()

    def test_pipe_watch2(self):
        self.client.set('foo', 'bar', self.expect(True))
        self.client.watch('foo', self.expect(True))
        self.client.set('foo', 'zar', self.expect(True))
        pipe = self.client.pipeline(transactional=True)
        pipe.get('foo')
        pipe.execute([self.pexpect([]), self.finish])
        self.start()

    def test_pipe_unwatch(self):
        self.client.set('foo', 'bar', self.expect(True))
        self.client.watch('foo', self.expect(True))
        self.client.set('foo', 'zar', self.expect(True))
        self.client.unwatch(callbacks=self.expect(True))
        pipe = self.client.pipeline(transactional=True)
        pipe.get('foo')
        pipe.execute([self.pexpect(['zar']), self.finish])
        self.start()

    def test_pipe_zsets(self):
        pipe = self.client.pipeline(transactional=True)

        pipe.zadd('foo', 1, 'a')
        pipe.zadd('foo', 2, 'b')
        pipe.zscore('foo', 'a')
        pipe.zscore('foo', 'b' )
        pipe.zrank('foo', 'a', )
        pipe.zrank('foo', 'b', )

        pipe.zrange('foo', 0, -1, True )
        pipe.zrange('foo', 0, -1, False)

        pipe.execute([
            self.pexpect([
                1, 1,
                1, 2,
                0, 1,
                [('a', 1.0), ('b', 2.0)],
                ['a', 'b'],
            ]),
            self.finish,
        ])
        self.start()

    def test_pipe_zsets2(self):
        pipe = self.client.pipeline(transactional=False)

        pipe.zadd('foo', 1, 'a')
        pipe.zadd('foo', 2, 'b')
        pipe.zscore('foo', 'a')
        pipe.zscore('foo', 'b' )
        pipe.zrank('foo', 'a', )
        pipe.zrank('foo', 'b', )

        pipe.zrange('foo', 0, -1, True )
        pipe.zrange('foo', 0, -1, False)

        pipe.execute([
            self.pexpect([
                1, 1,
                1, 2,
                0, 1,
                [('a', 1.0), ('b', 2.0)],
                ['a', 'b'],
            ]),
            self.finish,
        ])
        self.start()

    def test_pipe_hsets(self):
        pipe = self.client.pipeline(transactional=True)
        pipe.hset('foo', 'bar', 'aaa')
        pipe.hset('foo', 'zar', 'bbb')
        pipe.hgetall('foo')

        pipe.execute([
            self.pexpect([
                True,
                True,
                {'bar': 'aaa', 'zar': 'bbb'}
            ]),
            self.finish,
        ])
        self.start()

    def test_pipe_hsets2(self):
        pipe = self.client.pipeline(transactional=False)
        pipe.hset('foo', 'bar', 'aaa')
        pipe.hset('foo', 'zar', 'bbb')
        pipe.hgetall('foo')

        pipe.execute([
            self.pexpect([
                True,
                True,
                {'bar': 'aaa', 'zar': 'bbb'}
            ]),
            self.finish,
        ])
        self.start()

    def test_response_error(self):
        self.client.set('foo', 'bar', self.expect(True))
        self.client.llen('foo', [self.expect(ResponseError), self.finish])
        self.start()

class PubSubTestCase(TornadoTestCase):
    def setUp(self, *args, **kwargs):
        super(PubSubTestCase, self).setUp(*args, **kwargs)
        self.client2 = brukva.Client(io_loop=self.loop)
        self.client2.connection.connect()
        self.client2.select(9)

    def tearDown(self):
        super(PubSubTestCase, self).tearDown()
        del self.client2

    def assert_pubsub(self, msg, kind, channel, body):
        self.assertEqual(msg.kind, kind)
        self.assertEqual(msg.channel, channel)
        self.assertEqual(msg.body, body)

    def test_pub_sub(self):
        def on_recv(msg):
            self.assert_pubsub(msg, 'message', 'foo', 'bar')

        def on_subscription(msg):
            self.assert_pubsub(msg, 'subscribe', 'foo', 1)
            self.client2.listen(on_recv)

        self.client2.subscribe('foo', on_subscription)
        self.delayed(0.1, lambda:
            self.client2.set('gtx', 'rd', self.expect(RequestError)))
        self.delayed(0.2, lambda:
            self.client.publish('foo', 'bar',
                lambda *args: self.delayed(0.4, self.finish))
        )
        self.start()

    def test_pub_psub(self):
        def on_recv(msg):
            self.assert_pubsub(msg, 'pmessage', 'foo.*', 'bar')

        def on_subscription(msg):
            self.assert_pubsub(msg, 'psubscribe', 'foo.*', 1)
            self.client2.listen(on_recv)

        self.client2.psubscribe('foo.*', on_subscription)
        self.delayed(0.1, lambda:
            self.client2.set('gtx', 'rd', self.expect(RequestError)))
        self.delayed(0.3, lambda:
            self.client.publish('foo.1', 'bar')
        )
        self.delayed(0.3, lambda:
            self.client.publish('bar.1', 'zar',
                lambda *args: self.delayed(0.4, self.finish))
        )
        self.start()

    def test_unsubscribe(self):
        global c
        c = 0
        def on_recv(msg):
            if isinstance(msg, Exception):
                self.fail('Got unexpected exception: %s' % msg)

            global c
            if c == 0:
                self.assert_pubsub(msg, 'message', 'foo', 'bar')
            elif c == 1:
                self.assert_pubsub(msg, 'message', 'so', 'much')
            c += 1

        def on_subscription(msg):
            self.assert_pubsub(msg, 'subscribe', 'foo', 1)
            self.client2.listen(on_recv)

        self.client2.subscribe('foo', on_subscription)
        self.delayed(0.1, lambda: self.client.publish('foo', 'bar'))
        self.delayed(0.2, lambda: self.client2.subscribe('so',))
        self.delayed(0.3, lambda: self.client2.unsubscribe('foo'))
        self.delayed(0.4, lambda: self.client.publish('so', 'much'))
        self.delayed(0.5, lambda: self.client2.unsubscribe('so'))
        self.delayed(0.6, lambda: self.client2.set('zar', 'xar', [self.expect(True), self.finish]))
        self.start()


    def test_pub_sub_disconnect(self):
        def on_recv(msg):
            self.assertIsInstance(msg, brukva.exceptions.ConnectionError)

        def on_subscription(msg):
            self.assertEqual(msg.kind, 'subscribe')
            self.assertEqual(msg.channel, 'foo')
            self.assertEqual(msg.body, 1)
            self.client2.listen(on_recv)

        def on_publish(value):
            self.assertIsNotNone(value)

        self.client2.subscribe('foo', on_subscription)
        self.delayed(0.2, lambda: self.client2.disconnect())
        self.delayed(0.3, lambda: self.client.publish('foo', 'bar', on_publish))
        self.delayed(0.4, lambda: self.client2.publish('foo', 'bar', on_publish))
        self.delayed(0.5, self.finish)
        self.start()

class AsyncWrapperTestCase(TornadoTestCase):
    def test_wrapper(self):
        @process
        def simulate(client, callbacks):
            res = yield client.async.set('foo1', 'bar')
            self.assertEquals(res, True)
            res = yield client.async.set('foo2', 'zar')
            self.assertEquals(res, True)
            r1, r2 = yield [client.async.get('foo1'), client.async.get('foo2')]
            self.assertEquals(r1, 'bar')
            self.assertEquals(r2, 'zar')
            callbacks(None)
        self.loop.add_callback(lambda: simulate(self.client, self.finish))
        self.start()


class ReconnectTestCase(TornadoTestCase):
    def test_redis_timeout(self):
        self.client.set('foo', 'bar', self.expect(True))
        self.delayed(10, lambda:
            self.client.get('foo', [
                self.expect('bar'),
                self.finish
            ])
        )
        self.start()

    def test_redis_timeout_with_pipe(self):
        self.client.set('foo', 'bar', self.expect(True))
        pipe = self.client.pipeline(transactional=True)
        pipe.get('foo')

        self.delayed(10, lambda:
            pipe.execute([
                self.pexpect([
                    'bar',
                ]),
                self.finish,
            ])
        )
        self.start()

if __name__ == '__main__':
    unittest.main()
