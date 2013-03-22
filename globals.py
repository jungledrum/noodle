from werkzeug.local import LocalStack, LocalProxy
from functools import partial

def _get_object(name):
  request = request_stack.top
  return getattr(request, name)

def _params():
  request = request_stack.top
  return request.form

request_stack = LocalStack()

params = LocalProxy(_params)
path_params = LocalProxy(lambda :request_stack.top.path_params)
session = dict()
cookie = dict()

request = None
response = None
