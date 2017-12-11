from dit_flow.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType


class ReaderWidget(FlowWidget):

    def __init__(self, *args, **kwargs):
        super(ReaderWidget, self).__init__(*args, **kwargs)
        self.channel = 'ReaderWidget'
        self.do_it = True
        self.required_args = {'log_file': ''}
        self.required_arg_types = {'log_file': PortType.STR}

    def go(self, *args, **kwargs):
        super().go(*args, **kwargs)
        # Write out input and output columns to log file.
        self.logger.debug('{} reading input file.'.format(self.channel))
        result = self.widget_method(*args, **kwargs)
        return result
