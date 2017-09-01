from dit_flow.reader_widget import ReaderWidget
from dit_flow.flow_widget import FlowWidget

class WidgetFactory:
    '''
    Abstract class encapsulating generation of widgets
    '''

    factories = {}

    @staticmethod
    def addFactory(id, widgetFactory):
        WidgetFactory.factories.put[id] = widgetFactory

    @staticmethod
    def createWidget(id):
        if id not in WidgetFactory.factories.keys():
            WidgetFactory.factories[id] = eval(id + '.Factory()')
        return WidgetFactory.factories[id].create()

