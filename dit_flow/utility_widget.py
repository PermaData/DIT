from collections import OrderedDict
from circuits import Component


class UtilityWidget(Component):

    def __init__(self, *args, **kwargs):
        super(UtilityWidget, self).__init__(*args, **kwargs)
        self.channel = 'utility_widget'
        self.description = None
        self.input_args = OrderedDict()
        self.input_arg_types = OrderedDict()

    def go(self, *args, **kwargs):
        result = self.widget_method(*args, **kwargs)
        return result
