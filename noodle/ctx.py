import md5
from globals import _request_stack, SECRET_KEY
from wrappers import Cookie, Request

class RequestContext:
    def __init__(self, environ, app, db):
        self.app = app
        self.db = db
        self.request = Request(environ)
        self.cookie = Cookie()
        self.session = dict()
        self.route = None

    def push(self):
        top = _request_stack.top
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
                self.session[session_key] = session_value
            else:
                self.cookie.old[k] = v
        _request_stack.push(self)

    def pop(self):
        _request_stack.pop()

    def __enter__(self):
        self.push()
        # print '----------request_stack:', len(_request_stack._local.stack)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.db.remove()
        self.pop()
