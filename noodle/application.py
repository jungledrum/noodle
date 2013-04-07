# -*- coding:utf8 -*-
from route import *
from wrappers import Request, Response
from ctx import RequestContext
from globals import _app_stack, _request_stack, cookie, session, SECRET_KEY
import os.path
import md5

class App:
    def __init__(self):
        _app_stack.push(self)
        self.routes = []
        self._init_route()

    def _init_route(self):
        # 从用户的路由配置文件中加载路由config/route.py
        config_file = os.path.abspath('config/route.py')
        execfile(config_file)
        # print_routes(self.routes)

    def process_response(self, response):
        cookie.output(response)

        # session
        for k,v in session.items():
            session_key = 'SESSION' + k

            if v is None:
                response.delete_cookie(session_key)
            else:
                m = md5.new()
                m.update(SECRET_KEY)
                m.update(v)
                session_value = m.hexdigest() + '?' + v
                response.set_cookie(session_key, session_value)

        return response

    def dispatch_request(self):
        request = _request_stack.top.request
        path = request.path
        verb = request.method
        if request.form.has_key('_method'):
            verb = request.form['_method']

        route = find_route(self.routes, path, verb)
        request.route = route

        # 404
        if route is None:
            return Response('404', mimetype='text/html')

        # css/js/images
        if route.has_key('static') and route['static'] == True:
            file_path = route['file']
            with open(file_path) as f:
                    body = f.read()
            response = Response(body, mimetype=route['mimetype'])
        # xxx_controller.xxx()
        else:
            action = route['action']
            params = route['params']
            resource = route['resource']
            request.path_params = params
            package = 'app.controllers.' + resource + "_controller"
            controller = resource.capitalize() + "Controller"

            # from xxx_controller import *
            module = __import__(package, globals(), locals(), [''], -1)
            c = getattr(module, controller)()
            if c.before_filter is not None:
                for f in c.before_filter:
                    r = getattr(c, f)()
                    if r is not None:
                        return r
            method = getattr(c, action)

            response = method()

            if c.after_filter is not None:
                for f in c.after_filter:
                    r = getattr(c, f)()
                    if r is not None:
                        return r


        return response

    def __call__(self, environ, start_response):
        with self.request_context(environ):
            response = self.dispatch_request()
            response = self.process_response(response)
            return response(environ, start_response)

    def request_context(self, environ):
        return RequestContext(environ)

    def run(self, host='127.0.0.1', port=5000, **options):
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True, **options)