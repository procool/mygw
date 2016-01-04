import brukva
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
from brukva import adisp
import logging


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('app')


c = brukva.Client()
c.connect()


def on_set(result):
    log.debug("set result: %s" % result)


c.set('foo', 'Lorem ipsum #1', on_set)
c.set('bar', 'Lorem ipsum #2', on_set)
c.set('zar', 'Lorem ipsum #3', on_set)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @adisp.process
    def get(self):
        foo = yield c.async.get('foo')
        bar = yield c.async.get('bar')
        zar = yield c.async.get('zar')
        self.set_header('Content-Type', 'text/html')
        self.render("template.html", title="Simple demo", foo=foo, bar=bar, zar=zar)


application = tornado.web.Application([
    (r'/', MainHandler),
])


if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
