from collections import OrderedDict
from circuits import Component
from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


class FlowWidget(Component):

    def __init__(self, *args, **kwargs):
        super(FlowWidget, self).__init__(*args, **kwargs)
        self.channel = 'flow_widget'
        self.description = ''
        self.required_args = {}
        self.required_arg_types = {}
        self.input_args = OrderedDict()
        self.input_arg_types = OrderedDict()

    def setup_logger(self, name, log_file=None, log_level=DEFAULT_LOG_LEVEL):
        if name is None:
            name = self.channel
        self.logger = setup_logger(name, log_file=log_file, log_level=log_level)

    def go(self, *args, **kwargs):
        log_file = None
        log_level = DEFAULT_LOG_LEVEL
        if 'log_file' in kwargs.keys():
            log_file = kwargs['log_file']
        if 'log_level' in kwargs.keys():
            log_level = int(kwargs['log_level'])
        self.setup_logger(self.channel, log_file=log_file, log_level=log_level)

    def set_input_arg(self, arg_name, arg_value):
        self.input_args[arg_name] = arg_value

    def set_required_arg(self, arg_name, arg_value):
        if arg_name not in self.required_args.keys():
            message = '{} is not a required argument of {}'.format(arg_name, self.__class__)
            raise Exception(message)
        else:
            self.required_args[arg_name] = arg_value
