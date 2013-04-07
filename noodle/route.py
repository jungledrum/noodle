# -*- coding: utf-8 -*-
from globals import current_app
import os

class Rule:
    def __init__(self, path, verb, action):
        self.path = path
        self.verb = verb
        self.resource = action.split('#')[0]
        self.action = action.split('#')[1]
        self.length = path.count('/') 
        self.has_parameter = self._has_parameter()

    def _has_parameter(self):
        l = self.path.split('/')
        for t in l:
            if t.startswith(':'):
                return True
        return False

def rule(path, verb, action):
    r = Rule(path, verb, action)
    current_app.routes.append(r)

def resources(res):
    rule('/%s' % res, 'get', '%s#index' % res)
    rule('/%s/new' % res, 'get', '%s#new' % res)
    rule('/%s' % res, 'post', '%s#create' % res)
    rule('/%s/:id' % res, 'get', '%s#show' % res)
    rule('/%s/:id/edit' % res, 'get', '%s#edit' % res)
    rule('/%s/:id' % res, 'post', '%s#update' % res)
    rule('/%s/:id' % res, 'delete', '%s#destroy' % res)

def find_route(routes, path, verb):
    if path[len(path)-1] == '/' and len(path) > 1:
        path = path[0:len(path)-1]

    path_list = path.split('/')
    params = dict()

    # 完全匹配
    for r in routes:
      if r.path == path and r.verb.lower() == verb.lower():
          return {'resource': r.resource, 'action':r.action, 'params':{}}

    # 模糊匹配
    for r in routes:
        if r.verb.lower() != verb.lower() or r.length != path.count('/'):
            continue
        for i,v in enumerate(r.path.split('/')):
            if v.startswith(':'):
                params[v[1:]] = path_list[i]
            elif v == path_list[i]:
                continue
            else:
                params.clear()
                break
        if len(params) > 0:
            return {'resource':r.resource, 'action':r.action, 'params':params}

    # 静态文件
    public_path = os.path.abspath('public/')
    file_path = public_path + path
    if file_path.endswith('.css'):
        mimetype = 'text/css'
    elif file_path.endswith('.js'):
        mimetype = 'application/javascript'
    elif file_path.endswith('jpg'):
        mimetype = 'image/jpg'
    elif file_path.endswith('gif'):
        mimetype = 'image/gif'
    if os.path.exists(file_path):
        return {'static':True, 'file':file_path, 'mimetype':mimetype}


def print_routes(routes):
    for r in routes:
        print_route(r)

def print_route(r):
    print r.path.ljust(20),r.verb.ljust(6), r.action.ljust(15), str(r.length).ljust(2),\
            str(r.has_parameter).ljust(5)



if __name__ == '__main__':
    print_routes()
    print find_route('/posts/4', 'put')
