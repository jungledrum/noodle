from noodle.controller_base import *

class IndexController(ControllerBase):
    def index(self):
        return render('index.html')