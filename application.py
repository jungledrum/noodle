from werkzeug.wrappers import Response
from route import *
from request import *

def app(environ, start_response):
  print '-'*80
  Request(environ).push()
  request = request_stack.top
  path = request.path
  verb = request.method

  route = find_route(path, verb)
  action = route['action']
  params = route['params']
  request.path_params = params

  if action != None:
    resource = "posts"
    package = 'app.controllers.' + resource + "_controller"
    controller = resource.capitalize() + "Controller"

    # from posts_controller import *
    module = __import__(package, globals(), locals(), [''], -1)
    c = getattr(module, controller)()
    method = getattr(c, action)

    response = method()
  else:
    response = Response('404', mimetype='text/html')

  return response(environ, start_response)

if __name__ == '__main__':
  from werkzeug.serving import run_simple
  run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
