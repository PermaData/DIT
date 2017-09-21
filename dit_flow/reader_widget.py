from dit_flow.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType

class ReaderWidget(FlowWidget):

    def __init__(self, *args, **kwargs):
        super(ReaderWidget, self).__init__(*args, **kwargs)
        self.channel = 'ReaderWidget'
        self.do_it = True
        self.required_args = {'log_file': ''}
        self.required_arg_types = {'log_file': PortType.STR}
        self.logger = None

    def go(self, *args, **kwargs):
        print(self.channel, ' received go event')
        print(self.channel, ' args: ', args, '  kwargs:', kwargs)
        # Write out input and output columns to log file.
        result = self.widget_method(*args, **kwargs)
        return result
