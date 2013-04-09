from werkzeug.local import LocalStack, LocalProxy
from functools import partial

def _params():
    request = _request_stack.top.request
    return dict(request.form.items() + request.args.items() + request.path_params.items())

_request_stack = LocalStack()
_app_stack = LocalStack()

params = LocalProxy(_params)

current_app = LocalProxy(lambda :_app_stack.top)
request = LocalProxy(lambda :_request_stack.top.request)
cookie = LocalProxy(lambda :_request_stack.top.cookie)
session = LocalProxy(lambda :_request_stack.top.session)

SECRET_KEY = 'flkdsjalkfjdslafjklajf'

db = LocalProxy(lambda :_request_stack.top.db)



