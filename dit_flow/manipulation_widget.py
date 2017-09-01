from dit_flow.flow_widget import FlowWidget


class ManipulationWidget(FlowWidget):
    i_am_widget = 'ManipulationWidget'

    class Factory:
        def create(self):
            return ManipulationWidget()
