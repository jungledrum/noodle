import os
from jinja2 import Template, Environment, FileSystemLoader
from globals import *

def render(template_name, params={}):
    template_path = os.path.join(os.path.dirname(__file__), '../app/views/') + request.route['resource']
    env = Environment(loader=FileSystemLoader(template_path),
        autoescape=True)
    env.globals['session'] = session
    env.globals['cookie'] = cookie

    template = env.get_template(template_name)
    body = template.render(params)
    return Response(body, mimetype='text/html')


def render_text(body):
    return Response(body, mimetype='text/plain')

