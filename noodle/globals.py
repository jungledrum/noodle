from werkzeug.local import LocalStack, LocalProxy, Local
from functools import partial
from werkzeug.wrappers import Response

def _get_object(name):
  request = request_stack.top.request
  return getattr(request, name)

def _params():
  request = request_stack.top.request
  return request.form

request_stack = LocalStack()

params = LocalProxy(_params)
path_params = LocalProxy(lambda :request_stack.top.request.path_params)

request = LocalProxy(lambda :request_stack.top.request)
cookie = LocalProxy(lambda :request_stack.top.cookie)
session = LocalProxy(lambda :request_stack.top.session)

SECRET_KEY = 'flkdsjalkfjdslafjklajf'
