#!/usr/bin/env python
import argparse as ap
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


def file_choices_to_string(kwargs):
    pass


def dropdowns_to_string(kwargs):
    pass


def checkboxs_to_boolean(kwargs):
    pass


def string_to_file_choices(kwargs):
    pass


def string_to_dropdowns(kwargs):
    pass


def boolean_to_checkboxs(kwargs):
    pass


def parse_post(config, kwargs):
    file_choices_to_string(kwargs)
    dropdowns_to_string(kwargs)
    checkboxs_to_boolean(kwargs)



class Root(Controller):


    def GET(self, *args, **kwargs):
        return Templates.serve_template(tpl, configs=configs, config=config_translator.config, widget=config_translator.widget)
        # return render(self.tpl, configs=page_args)

class Add(Controller):

    channel = "/add"
    this_config = {}

    def POST(self, *args, **kwargs):
        print('begin post: ', self.this_config)
        config_translator.deep_update(self.this_config, config_translator.config)
        config_translator.deep_update(self.this_config, kwargs)
        print('before return: ', self.this_config)
        return Templates.serve_template(tpl, configs=configs, config=self.this_config, widget=config_translator.widget)


    def GET(self, *args, **kwargs):
        return Templates.serve_template(tpl, configs=configs, config=config_translator.config, widget=config_translator.widget)


def run_server(host, port):
    app = Server((host, port))
    Logger().register(app)
    Static("/static", docroot="dit_gui/static").register(app)
    Root().register(app)
    Add().register(app)
    # widgets.Widgets().register(app)
    # step.StepOrder().register(app)
    # steps.Steps().register(app)
    app.run()

def parse_arguments():
    parser = ap.ArgumentParser(description='Runs the DIT GUI.')

    parser.add_argument('-s', '--host', default='0.0.0.0', help='The hostname to bind to for the server.')
    parser.add_argument('-p', '--port', type=int, default=8000, help='The port to bind to for the server.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    run_server(args.host, args.port)
