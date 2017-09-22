from dit_flow.flow_widget import FlowWidget


class WriterWidget(FlowWidget):


    def __init__(self, *args, **kwargs):
        super(WriterWidget, self).__init__(*args, **kwargs)
        self.channel = 'writer_widget'

    def go(self, *args, **kwargs):
        # Write out input and output columns to log file.
        result = self.widget_method(*args, **kwargs)
        return result
