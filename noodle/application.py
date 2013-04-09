# -*- coding:utf8 -*-
from route import *
from wrappers import Request, Response
from ctx import RequestContext
from globals import _app_stack, _request_stack, request, session, cookie, params, SECRET_KEY,db, current_app
import os.path
import md5
import random
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.orm.scoping import scoped_session
from datetime import datetime

class App:
    def __init__(self):
        _app_stack.push(self)
        print '>>>','init_app'
        self.routes = []
        self._init_route()
        self._init_db()

    def _init_db(self):
        print '>>>', 'init_db'
        db_config_file = os.path.abspath('config/database.py')
        # execfile(db_config_file)
        db_info = {'username':'root', 
           'password':'123456',
           'host':'127.0.0.1',
           'db':'storm'}

        engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8' % (db_info['username'], db_info['password'], db_info['host'], db_info['db']),
                                echo=False)
        # Session = sessionmaker(bind=engine)
        self.db = scoped_session(sessionmaker(bind=engine))

    def _init_route(self):
        print '>>>', 'init_route'
        # 从用户的路由配置文件中加载路由config/route.py
        config_file = os.path.abspath('config/route.py')
        execfile(config_file)
        # print_routes(self.routes)

    def check_csrf_token(self):
        request = _request_stack.top.request
        token = request.headers.get('X-CSRF-Token', None) or request.form.get('csrf_token', None)
        if request.method != 'GET':
            if not session.has_key('csrf_token') or token == None:
                return False
            if session['csrf_token'] != token:
                return False
            else:
                return True
        else:
            return True

    def write_csrf_token(self):
        token = str(random.random())
        session['csrf_token'] = token

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
        if self.check_csrf_token() == False:
            return Response('csrf', mimetype='text/html')
        

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
            self.write_csrf_token()
            
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
        with self.request_context(environ, self, self.db):
            response = self.dispatch_request()
            response = self.process_response(response)
            return response(environ, start_response)

    def request_context(self, environ, app, db):
        return RequestContext(environ, app, db)

    def run(self, host='127.0.0.1', port=5000, **options):
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger=True, use_reloader=True, **options)