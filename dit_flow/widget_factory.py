from dit_flow.reader_widget import ReaderWidget
from dit_flow.flow_widget import FlowWidget
from dit_flow.manipulation_widget import ManipulationWidget
from stringcase import pascalcase

class WidgetFactory:
    '''
    Abstract class encapsulating generation of widgets
    '''

    factories = {}

    @staticmethod
    def add_factory(id, widgetFactory):
        WidgetFactory.factories.put[id] = widgetFactory

    @staticmethod
    def has_factory(id):
        return id in WidgetFactory.factories.keys()

    @staticmethod
    def create_widget(id):
        if not WidgetFactory.has_factory(id):
            WidgetFactory.add_factory(id, type(pascalcase(id), (BaseClass,), {"__init__": __init__}))
        return WidgetFactory.factories[id].create()

