# -*- coding:utf8 -*-
import os
from globals import *
from wrappers import Response
import json
from mako.template import Template
from mako.lookup import TemplateLookup


def render(template_name, **params):
    params['session'] = session
    params['cookie'] = cookie
    params['get_flash'] = get_flash
    params['button'] = button
    params['get_csrf_token'] = get_csrf_token

    template_path = os.path.abspath('app/views/' + request.route['resource']) + '/'
    view_path = os.path.abspath('app/views/')
    lookup = TemplateLookup([template_path, view_path])
    
    template = Template(filename=template_path+template_name, input_encoding='utf-8',
                        output_encoding='utf-8', default_filters=['h'], lookup=lookup, uri='/')
    body = template.render(**params)

    return Response(body, mimetype='text/html')


def render_text(body):
    return Response(body, mimetype='text/plain')

def render_html():
    pass

def render_json(body):
    # body = json.dumps(o[1].__dict__)
    return Response(body, mimetype='application/json')

def get_flash():
    f = session.get('flash', '')
    session['flash'] = None
    return f

def button(value="button"):
    s = u'<button>%s</button>' % value.decode('utf8')
    return s

def get_csrf_token():
    return session['csrf_token']

