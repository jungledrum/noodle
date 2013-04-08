# -*- coding:utf8 -*-
from noodle.controller_base import *

class LoginController(ControllerBase):

    def new(self):
        if session.has_key('username'):
            return redirect('/')
        return render('new.html')

    def create(self):
        username = params['username']
        password = params['password']

        user = User.where("username='%s' and password='%s'" % (username, password)).first()
        if user is not None:
            session['username'] = user.username
            session['flash'] = 'welcome! %s' % session['username']
            return redirect('/')
        else:
            session['flash'] = 'login fail...'
            return redirect('/login')

    def logout(self):
        session['username'] = None
        return redirect('/')
