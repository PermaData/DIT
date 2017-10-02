import os
import glob

from circuits.web import Controller
from sys import path
from os.path import dirname as dir

path.append(dir(path[0]))
from widget_loader import WidgetLoader

class Widget(Controller):

    channel = '/widget'

    def GET(self):
        for filepath in glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dit_flow", "dit_widget"), "*.py"):
            print("Found file: ", filepath)
            name = os.path.splitext(os.path.basename(filepath))[0]
            # add package prefix to name, if required
            module = __import__(name)
            for member in dir(module):
                print(member)
