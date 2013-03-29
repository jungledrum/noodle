from werkzeug.wrappers import Request as RequestBase
from werkzeug.utils import redirect
from globals import *


class Request(RequestBase):

  path_params = None

  def push(self):
    request_stack.push(self)


