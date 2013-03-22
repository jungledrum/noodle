# -*- coding: utf-8 -*-
routes = [] 

class Rule:
  def __init__(self, path, verb, action):
    self.path = path
    self.verb = verb
    self.action = action
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
  routes.append(r)

rule('/', 'get', 'index')
rule('/posts', 'get', 'index')
rule('/posts/new', 'get', 'new')
rule('/posts', 'post', 'create')
rule('/posts/:id', 'get', 'show')
rule('/posts/:id/edit', 'get', 'edit')
rule('/posts/:id', 'post', 'update')
rule('/posts/:id', 'delete', 'destroy')


def find_route(path, verb):
  if path[len(path)-1] == '/' and len(path) > 1:
    path = path[0:len(path)-1]

  path_list = path.split('/')
  params = dict()

  # 完全匹配
  for r in routes:
    if r.path == path and r.verb.lower() == verb.lower():
      return {'action':r.action, 'params':{}}

  # 模糊匹配
  for r in routes:
    if r.verb.lower() != verb.lower() or r.length != path.count('/'):
      continue
    for i,v in enumerate(r.path.split('/')):
      if v.startswith(':'):
        params[v] = path_list[i]
      elif v == path_list[i]:
        continue
      else:
        params.clear()
        break
    if len(params) > 0:
      return {'action':r.action, 'params':params}

def print_routes():
  for r in routes:
    print_route(r)

def print_route(r):
  print r.path.ljust(20),r.verb.ljust(6), r.action.ljust(15), str(r.length).ljust(2),\
        str(r.has_parameter).ljust(5)



if __name__ == '__main__':
  print_routes()
  print find_route('/posts/4', 'put')
