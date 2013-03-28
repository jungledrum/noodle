from hummingbird.controller_base import *

class LoginController(ControllerBase):

    def new(self):
        return render('new.html')

    def create(self):
        username = params['username']
        password = params['password']

        user = User.where("username='%s' and password='%s'" % (username, password)).first()
        if user is not None:
            session['username'] = user.username
            return redirect('/')
        else:
            return render_text("no user %s" % username)

    def logout(self):
        session['username'] = None
        return redirect('/')
