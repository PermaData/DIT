#!/usr/bin/env python
import os

from mako.lookup import TemplateLookup

from dit_gui.widget import *
from dit_gui.step import *
from dit_gui.flow import *
# from dit_gui.connection import *
from circuits.web import Controller, Logger, Server, Static
from dit_gui.templates import Templates


class Root(Controller):

    tpl = "index.html"
    attributes = {
            'stepOrder': [],
            'stepDefinitions': [],
            'files': [],
            'variableMapFile': [],
            'missingValues': []
    }

    def GET(self, *args, **kwargs):
        return Templates.serve_template(self.tpl, **kwargs)


    def submit(self, stepOrder, stepDefinition, files, variableMapFile, missingValues):
        self.attributes['stepOrder'].extend(stepOrder)
        self.attributes['stepDefinitions'].extend(stepDefinition)
        self.attributes['files'].extend(files)
        self.attributes['variableMapFile'].extend(variableMapFile)
        self.attributes['missingValues'].extend(missingValues)
        return render(self.tpl, attributes=self.attributes)


app = Server(("0.0.0.0", 8000))
Logger().register(app)
Static(docroot="static").register(app)
Root().register(app)
widgets.Widgets().register(app)
step.StepOrder().register(app)
steps.Steps().register(app)
app.run()
