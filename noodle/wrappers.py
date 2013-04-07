from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase
from werkzeug.utils import redirect
from globals import *
import md5


class Request(RequestBase):

    path_params = None

    def push(self):
        request_stack.push(self)

class Response(ResponseBase):
    pass


class Cookie(dict):

    _del = []
    _old = {}
    _new = {}
    
    def __setitem__(self, k ,v):
        if self._old.has_key(k):
            del self._old[k]
        self._new[k] = v

    def __getitem__(self, k):
        if self._old.has_key(k):
            return self._old[k]
        else:
            return self._new[k]

    def __delitem__(self, k):
        if self._old.has_key(k):
            del self._old[k]
        elif self._new.has_key(k):
            del self._new[k]
        self._del.append(k)

    def output(self, response):
        for k,v in self._new.items():
            # print 'set %s = %s' % (k,v)
            response.set_cookie(k, v, 3600*24*7)
        for i in self._del:
            # print 'del %s' % i
            response.delete_cookie(k)
