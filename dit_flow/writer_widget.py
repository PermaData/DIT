from dit_flow.flow_widget import FlowWidget


class WriterWidget(FlowWidget):


    def __init__(self, *args, **kwargs):
        super(WriterWidget, self).__init__(*args, **kwargs)
        self.channel = 'WriterWidget'

    def go(self):
        print(self.channel, ' received go event')
        # Write out input and output columns to log file.
        result = self.widget_method(*self.input_args, **self.required_args)
        return result
