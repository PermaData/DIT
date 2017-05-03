from circuits.web import Controller
from templates import Templates

class Steps(Controller):

    channel = '/steps'
    tpl = 'steps.html'

    step_list = ['Fred', 'Ginger', 'Monjula']

    def GET(self, *args, **kwargs):
        print("Inside Steps GET")
        kwargs.update({'step_list': self.step_list})
        print(kwargs)
        return Templates.serve_template(self.tpl, **kwargs)

    def POST(self, *args, **kwargs):
        print("Inside Steps POST")
        return "%r %r" % (args, kwargs)

    def PUT(self, *args, **kwargs):
        print("Inside Steps PUT")
        return "%r %r" % (args, kwargs)
