import os
from jinja2 import Template, Environment, FileSystemLoader
from werkzeug.wrappers import Response

template_path = os.path.join(os.path.dirname(__file__), 'app/views')
print template_path
env = Environment(loader=FileSystemLoader(template_path),
        autoescape=True)

def render(template_name, params):
  template = env.get_template(template_name)
  body = template.render(params)
  response = Response(body, mimetype='text/html')
  return response
