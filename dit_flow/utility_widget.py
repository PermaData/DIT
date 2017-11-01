from collections import OrderedDict
from circuits import Component

from dit_flow.dit_widget.common.setup_logger import setup_logger

class UtilityWidget(Component):


    def __init__(self, *args, **kwargs):
        super(UtilityWidget, self).__init__(*args, **kwargs)
        self.channel = 'utility_widget'
        self.description = None
        self.input_args = OrderedDict()
        self.input_arg_types = OrderedDict()


    def setup_logger(self, name, log_file):
        if name is None:
            name = self.channel
        self.logger = setup_logger(name, log_file)


    def go(self, *args, **kwargs):
        log_file = None
        if 'log_file' in kwargs.keys():
            log_file = kwargs['log_file']
        self.setup_logger(self.channel, log_file)
        result = self.widget_method(*args, **kwargs)
        return result
