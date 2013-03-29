from hummingbird.application import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':
  app = App()
  # http_server = HTTPServer(WSGIContainer(app))
  # http_server.listen(5000)
  # IOLoop.instance().start()
  app.run('192.168.1.100')