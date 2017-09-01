from dit_flow.flow_widget import FlowWidget

class ReaderWidget(FlowWidget):
    i_am_widget = 'ReaderWidget'

    class Factory:
        def create(self):
            return ReaderWidget()
