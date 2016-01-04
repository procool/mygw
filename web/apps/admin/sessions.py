import logging
import os
import redis
import string, random


class RedisSessions(object):
    expire = None
    session_size=16

    ##redis_ident = os.path.abspath('')
    redis_ident = 'mygw_sessions_'
    redis = redis.Redis()

    @staticmethod
    def token_gen(size=16):
        chars=string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))


    @classmethod
    def __get(cls_, key, ident=None):
        if ident is not None:
            key = "%s_%s" % (ident, key)
        return cls_.redis.get(cls_.redis_ident + key)

    @classmethod
    def __set(cls_, key, val, expire=None, ident=None):
        if ident is not None:
            key = "%s_%s" % (ident, key)
        if expire is None:
            return cls_.redis.set(cls_.redis_ident + key, val)
        ##logging.error('SESSION: %s' % (cls_.redis_ident + key))
        return cls_.redis.setex(cls_.redis_ident + key, val, expire)


    @classmethod
    def __del(cls_, key, ident=None):
        if ident is not None:
            key = "%s_%s" % (ident, key)
        return cls_.redis.delete(cls_.redis_ident + key)


    @classmethod
    def check(cls_, session, uid=None):
        uid_ = cls_.__get(session, ident='s2u')
        if uid_ is None:
            return None

        if uid is not None:
            if uid != uid_:
                return None

        ## Update session expire:
        cls_.store(uid_, session)
        return uid_


    @classmethod
    def get(cls_, uid):
        sess_ = cls_.__get(uid, ident='u2s')
        if sess_ is None:
            return cls_.create(uid)
        else:
            cls_.store(uid, sess_)
        return sess_



    @classmethod
    def create(cls_, uid):
        cls_.delete(uid)
        sess_ = cls_.token_gen(size=cls_.session_size)
        cls_.store(uid, sess_)
        return sess_


    @classmethod
    def store(cls_, uid, session):
        cls_.__set(uid, session, ident='u2s', expire=cls_.expire)
        cls_.__set(session, uid, ident='s2u', expire=cls_.expire)


    @classmethod
    def delete(cls_, uid):
        sess_ = cls_.__get(uid, ident='u2s')
        cls_.__del(uid, ident='u2s')
        cls_.__del(sess_, ident='s2u')



class Sessions(RedisSessions):
    expire = 600
    #expire = 60
    session_size=32

