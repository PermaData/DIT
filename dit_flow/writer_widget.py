from dit_flow.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType


class WriterWidget(FlowWidget):

    def __init__(self, *args, **kwargs):
        super(WriterWidget, self).__init__(*args, **kwargs)
        self.channel = 'writer_widget'
        self.do_it = True
        self.required_args = {'log_file': ''}
        self.required_arg_types = {'log_file': PortType.STR}

    def go(self, *args, **kwargs):
        super().go(*args, **kwargs)
        self.logger.debug('{} writing output file.'.format(self.channel))
        result = self.widget_method(*args, **kwargs)
        return result
