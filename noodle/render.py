import os
from jinja2 import Template, Environment, FileSystemLoader
from globals import *
from wrappers import Response
import json

def render(template_name, params={}):
    template_path = os.path.join(os.path.dirname(__file__), '../app/views/') + request.route['resource']
    env = Environment(loader=FileSystemLoader(template_path),
        autoescape=True)
    env.globals['session'] = session
    env.globals['cookie'] = cookie
    env.globals.update(get_flash = get_flash)

    template = env.get_template(template_name)
    body = template.render(params)
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

