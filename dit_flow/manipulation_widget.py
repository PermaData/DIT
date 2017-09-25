from dit_flow.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType


class ManipulationWidget(FlowWidget):

    def __init__(self, *args, **kwargs):
        super(ManipulationWidget, self).__init__(*args, **kwargs)
        self.channel = 'manipulation_widget'

        self.do_it = True
        self.required_args = {'input_data_file': '', 'output_data_file': '', 'log_file': ''}
        self.required_arg_types = {'input_data_file': PortType.STR,
                              'output_data_file': PortType.STR,
                              'log_file': PortType.STR}
        self.input_columns = []
        self.output_columns = []
        self.with_header = False
        if 'log_file' in kwargs.keys():
            self.logger = self.setup_logger(self.channel, kwargs['log_file'])
        else:
            self.logger = self.setup_logger(self.channel, self.channel + '.log')

    def go(self):
        # Write out input and output columns to log file.
        self.logger.info('Running ', self.channel, ' on input columns: ', self.input_columns, '  to output columns: ', self.output_columns)
        result = self.widget_method(*self.input_args, **self.required_args)
        return result
