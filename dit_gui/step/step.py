from mako.template import Template
from circuits.web import Controller
from templates import Templates
import requests

class StepOrder(Controller):

    channel = '/step_order'
    tpl = 'step_order.html'
    __order_number = None

    @property
    def order_number(self):
        return self.__order_number

    @order_number.setter
    def order_number(self, new_order_number):
        self.__order_number = new_order_number

    def GET(self, *args, **kwargs):
        kwargs.update({'step_order': self.step_order})
        return Templates.serve_template(self.tpl, **kwargs)

    def POST(self, *args, **kwargs):
        data = self.request.body.read().decode('UTF-8')
        print(data)
        return "%r %r" % (args, kwargs)

    def PUT(self, *args, **kwargs):
        return "%r %r" % (args, kwargs)

class StepDefinition(Controller):

    channel = '/step_definition'
    tpl = 'step_defn.html'

    def GET(self, *args, **kwargs):
        return Templates.serve_template(self.tpl, **kwargs)

    def POST(self, *args, **kwargs):
        data = self.request.body.read().decode('UTF-8')
        print(data)
        return "%r %r" % (args, kwargs)

    def PUT(self, *args, **kwargs):
        return "%r %r" % (args, kwargs)
