from request import *
import md5
from globals import *

class RequestContext:
  def __init__(self, environ):
    self.request = Request(environ)
    self.cookie = dict()
    self.session = dict()
    self.route = None

  def push(self):
    top = request_stack.top
    if top is not None:
      top.pop()

    for k,v in self.request.cookies.iteritems():
      if k.startswith('SESSION'):
        session_key = k[7:]
        session_secret = v.split('?')[0]
        session_value = v.split('?')[1]
        m = md5.new()
        m.update(SECRET_KEY)
        m.update(session_value)
        if m.hexdigest() != session_secret:
          print 'session error---'
          continue
        self.session[session_key] = {'value':session_value, 'old_value':session_value}
      else:
        self.cookie[k] = {'value':v, 'old_value':v}
    request_stack.push(self)

  def pop(self):
    request_stack.pop()

  def __enter__(self):
    self.push()
    return self

  def __exit__(self, exc_type, exc_value, tb):
    self.pop()
