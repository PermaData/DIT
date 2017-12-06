#!/usr/bin/env python
import os
import json

from dit_gui.widget import *
from dit_gui.step import *
# from dit_gui.flow import *
# from dit_gui.connection import *
from widget_factory import WidgetFactory, widget_configs_by_type
from circuits.web import Controller, Logger, Server, Static
# from circuits.web.wsgi import Application
from dit_gui.templates import Templates

tpl = "index.html"

widget_factory = WidgetFactory()
configs = widget_configs_by_type(widget_factory.loader)
config_translator = widget_factory.create_widget('config_translator')


class Root(Controller):


    def GET(self, *args, **kwargs):
        return Templates.serve_template(tpl, configs=configs, config=config_translator.config, widget=config_translator.widget)
        # return render(self.tpl, configs=page_args)

class Add(Controller):

    channel = "/add"
    this_config = {}

    def POST(self, *args, **kwargs):
        print('config: ', self.this_config)
        print('kwargs: ', kwargs)
        config_translator.deep_update(self.this_config, config_translator.config)
        config_translator.deep_update(self.this_config, kwargs)
        print('config after: ', self.this_config)
        return Templates.serve_template(tpl, configs=configs, config=self.this_config, widget=config_translator.widget)


    def GET(self, *args, **kwargs):
        return Templates.serve_template(tpl, configs=configs, config=config_translator.config, widget=config_translator.widget)


app = Server(("0.0.0.0", 8000))
Logger().register(app)
Static("/static", docroot="dit_gui/static").register(app)
Root().register(app)
Add().register(app)
# widgets.Widgets().register(app)
# step.StepOrder().register(app)
# steps.Steps().register(app)
app.run()
