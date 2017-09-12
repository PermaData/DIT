from collections import OrderedDict
from dit_flow.dit_widget.port import PortType

class FlowWidget(object):

    channel = 'flow_widget'
    description = None
    required_args = {'input_data_file': '', 'output_data_file': '', 'log_file': ''}
    required_arg_types = {'input_data_file': PortType.STR,
                          'output_data_file': PortType.STR,
                          'log_file': PortType.STR}
    input_args = OrderedDict()
    input_arg_types = OrderedDict()
    widget_method = None

    def __init__(self):
        print('in flow_widget.__init__')

    def speak(self):
        print("I say: ", self.channel)

    def go(self):
        print(self.channel, ' received go event')
        result = self.widget_method(*self.input_args, **self.required_args)
        return result

