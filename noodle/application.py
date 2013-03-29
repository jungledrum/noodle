# -*- coding:utf8 -*-
from werkzeug.wrappers import Response
from route import *
from request import *
from ctx import RequestContext
from globals import *
import md5

class App:
  def __init__(self):
    pass

  def process_response(self, response):
    # 设置cookie，判断是否是request带来的cookie
    # 支持字符串和哈希两种值
    # todo：删除cookie
    for k,v in cookie.iteritems():
      if isinstance(v ,dict):
        if 'old_value' not in v:
          response.set_cookie(k, v['value'], 3600*24*7)
      else:
        response.set_cookie(k, v, 3600*24*7)

    # session
    for k,v in session.iteritems():
      session_key = 'SESSION' + k
      if v is None:
        response.delete_cookie(session_key)
      elif isinstance(v ,dict):
        if 'old_value' not in v:
          m = md5.new()
          m.update(SECRET_KEY)
          m.update(v['value'])
          session_value = m.hexdigest() + '?' + v['value']
          response.set_cookie(session_key, session_value)
      else:
        m = md5.new()
        m.update(SECRET_KEY)
        m.update(v)
        session_value = m.hexdigest() + '?' + v
        response.set_cookie(session_key, session_value)

    return response

  def dispatch_request(self):
    request = request_stack.top.request
    path = request.path
    verb = request.method
    if request.form.has_key('_method'):
      verb = request.form['_method']

    route = find_route(path, verb)
    request.route = route
    print '-'*100
    print route

    if route is None:
        return Response('404', mimetype='text/html')

    if route.has_key('static') and route['static'] == True:
        file_path = route['file']
        with open(file_path) as f:
            body = f.read()
        response = Response(body, mimetype=route['mimetype'])
    else:
        action = route['action']
        params = route['params']
        resource = route['resource']
        request.path_params = params
        package = 'app.controllers.' + resource + "_controller"
        controller = resource.capitalize() + "Controller"

        # from posts_controller import *
        module = __import__(package, globals(), locals(), [''], -1)
        c = getattr(module, controller)()
        method = getattr(c, action)

        response = method()

    return response

  def __call__(self, environ, start_response):
    with self.request_context(environ):
      response = self.dispatch_request()
      response = self.process_response(response)
      return response(environ, start_response)

  def request_context(self, environ):
    return RequestContext(environ)

  def run(self, host='127.0.0.1', port=5000):
    from werkzeug.serving import run_simple
    run_simple(host, port, self, use_debugger=True, use_reloader=True)
