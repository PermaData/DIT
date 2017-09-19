from dit_flow.flow_widget import FlowWidget

class ReaderWidget(FlowWidget):

    def __init__(self, *args, **kwargs):
        super(ReaderWidget, self).__init__(*args, **kwargs)
        self.channel = 'ReaderWidget'

    def go(self, *args, **kwargs):
        print(self.channel, ' received go event')
        # Write out input and output columns to log file.
        result = self.widget_method(*args, **kwargs)
        return result
