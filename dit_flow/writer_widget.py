from dit_flow.flow_widget import FlowWidget


class WriterWidget(FlowWidget):

    i_am_widget = 'WriterWidget'

    class Factory:
        def create(self):
            return WriterWidget()