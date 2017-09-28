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


    @staticmethod
    def input_and_output_columns_exist(input_columns, output_columns):
        columns_exist = True
        if input_columns is None:
            columns_exist = False
        elif len(input_columns) == 0:
            columns_exist = False
        elif output_columns is None:
            columns_exist = False
        elif len(output_columns) == 0:
            columns_exist = False
        return columns_exist


    def go(self, *args, **kwargs):
        super().go(*args, **kwargs)
        # Write out input and output columns to log file.
        if not ManipulationWidget.input_and_output_columns_exist(self.input_columns, self.output_columns):
            self.logger.info('Running ' + self.channel + ' without input and output data.')
        else:
            self.logger.info('Running ' + self.channel + ' on input columns: ' + str(self.input_columns) + '  to output columns: ' + str(self.output_columns))
        result = self.widget_method(*self.input_args.values(), **self.required_args)
        return result
