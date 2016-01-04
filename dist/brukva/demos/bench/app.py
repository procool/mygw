import brukva
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import redis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

r = redis.Redis(REDIS_HOST, REDIS_PORT, db=9)

c = brukva.Client(REDIS_HOST, REDIS_PORT)
c.connect()
c.select(9)

c.set('foo', 'bar')
c.set('foo2', 'bar2')


class BrukvaHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @brukva.adisp.process
    def get(self):
        foo, foo2 = yield [c.async.get('foo'), c.async.get('foo2')]
        self.set_header('Content-Type', 'text/plain')
        self.write(foo)
        self.write(foo2)
        self.finish()


class RedisHandler(tornado.web.RequestHandler):
    def get(self):
        foo = r.get('foo')
        foo2 = r.get('foo2')
        self.set_header('Content-Type', 'text/plain')
        self.write(foo)
        self.write(foo2)
        self.finish()


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello world!')
        self.finish()


application = tornado.web.Application([
    (r'/brukva', BrukvaHandler),
    (r'/redis', RedisHandler),
    (r'/hello', HelloHandler),
])


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
