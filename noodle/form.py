# -*- coding:utf8 -*-

class Form:

    errors = {}
    args = {}

    def validates(self, *args, **rules):
        for arg in args:
            if self.args.get(arg) != None:
                self.args[arg] = dict(self.args[arg].items() + rules.items())
            else:
                self.args[arg] = rules
            


    def is_valid(self, request):
        for k, v in self.args.items():
            for x, y in v.items():
                # print k,x,y
                func = getattr(self, x)
                if request.get(k) != None:
                    r = func(request[k], **y)
                    if r != None:
                        self.errors[k] = r
                else:
                    self.errors[k] = '%s is null' % k

        if len(self.errors) > 0:
            return False
        else:
            return True

    def length(self, arg, min=None, max=None):
        l = len(arg)
        if l<min or l>max:
            return 'must be %s<x<%s' % (min,max)

    def not_empty(self, arg):
        r = len(arg.strip())
        if r<1:
            return 'can not be empty'

# test
form = Form()
form.validates('name', 'passwd', length={'min':3, 'max':8})
form.validates('name', not_empty={})


request = {'name':'', 'passwd':'dd1'}
# print form.args
print form.is_valid(request)
print form.errors