#!/usr/bin/env python
import os

import mako
from mako.lookup import TemplateLookup

from circuits.web import Controller

class StepOrder(Controller):

    channel = "/step_order"

    def POST(self, *args, **kwargs): #***
        return "%r %r" % (args, kwargs)
