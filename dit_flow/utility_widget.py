from collections import OrderedDict
from circuits import Component

class UtilityWidget(Component):

    channel = 'utility_widget'
    description = None
    input_args = OrderedDict()
    input_arg_types = OrderedDict()
    widget_method = None

    def __init__(self):
        super(UtilityWidget, self).__init__()

    def go(self, event, *args, **kwargs):
        event.stop()
        print(self.channel, ' received go event')
        print('go arguments: ', *args, '  kwargs: ', **kwargs)
        # result = self.widget_method(*self.input_args, **self.required_args)
        result = self.widget_method(*args, **kwargs)
        return result
