import inspect
import os
import glob
import pydoc
import sys
from os.path import dirname as dir

sys.path.append(dir(sys.path[0]))

from circuits.web import Controller
from widget_loader import WidgetLoader

class Widgets(Controller):

    channel = '/widgets'

    def GET(self, *args, **kwargs):
        signatures = list()
        sys.path.append('/Users/hwilcox/Workspace/dit-3.0')
        print(sys.modules)
        members = inspect.getmembers(sys.modules['dit_flow.dit_widget'])
        widget_names = list()
        for member_key, member_value in members:
            # find widgets imported
            if member_key == '__all__':
                widget_names = member_value
                continue
            for widget_name in widget_names:
                try:
                    # Attempt import
                    mod = __import__(widget_name)
                    if mod is None:
                       print("Module not found")

                    # Module imported correctly, let's create the docs
                    list.append(self.getmarkdown(mod))
                except pydoc.ErrorDuringImport as e:
                    print("Error while trying to import " + widget_name)
        return signatures

    def getmarkdown(self, module):
        output = list()
        output.extend(self.getfunctions(module))
        output.append("***\n")
        #output.extend(getclasses(module))
        return "".join(output)

    def getclasses(self, item):
        output = list()
        for cl in inspect.getmembers(item, inspect.isclass):
            if cl[0] != "__class__" and not cl[0].startswith("_"):
                # Consider anything that starts with _ private
                # and don't document it
                output.append(cl[0])
                # Get the docstring
                output.append(inspect.getdoc(cl[1]))
                # Get the functions
                output.extend(self.getfunctions(cl[1]))
                # Recurse into any subclasses
                output.extend(self.getclasses(cl[1]))
        return output

    def getfunctions(self, item):
        output = list()
        for func in inspect.getmembers(item, inspect.isfunction):
            output.append(func[0])
            # Get the signature
            output.append("\n```python\n")
            output.append(func[0])
            output.append(str(inspect.signature(func[1])))
            # Get the docstring
            output.append(inspect.getdoc(func[1]))
        return output
