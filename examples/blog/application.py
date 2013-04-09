import sys
sys.path.append('../../../noodle/')
from noodle.application import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':

    app = App()
    # http_server = HTTPServer(WSGIContainer(app))
    # http_server.listen(5001)
    # IOLoop.instance().start()
    app.run(threaded=True)
    app.run(port=5001)

    # app.run(processes=50)
    # app.run()
