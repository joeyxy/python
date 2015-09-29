#!/usr/bin/env python

from gevent import monkey;monkey.patch_all()
from gevent.wsgi import WSGIServer
import gevent
import tornado
import tornado.web
import tornado.wsgi

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')


def app(env,start_response):
    start_response('200 ok',[('Content-Type','text/html')])
    return ["<b>Hello world and all</b>"]



if __name__ == "__main__":
    application = tornado.wsgi.WSGIApplication(hadnlers=[(r"/",IndexHandler)])
    server=gevent.wsgi.WSGIServer(('',8000),app)
    server.serve_forever()