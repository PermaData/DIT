from collections import OrderedDict
from circuits import Component

class FlowWidget(Component):


    def __init__(self, *args, **kwargs):
        super(FlowWidget, self).__init__(*args, **kwargs)
        self.channel = 'flow_widget'
        self.description = ''
        self.required_args = {}
        self.required_arg_types = {}
        self.input_args = OrderedDict()
        self.input_arg_types = OrderedDict()


    def set_input_arg(self, arg_name, arg_value):
        self.input_args[arg_name] = arg_value


    def set_required_arg(self, arg_name, arg_value):
        if arg_name not in self.required_args.keys():
            message = '{} is not a required argument of {}'.format(arg_name, self.__class__)
            self.logger.error(message)
            raise Exception(message)
        else:
            self.required_args[arg_name] = arg_value
