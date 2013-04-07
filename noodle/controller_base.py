from render import *
from request import *
from app.models import *

class ControllerBase:

    before_filter = None
    after_filter = None
