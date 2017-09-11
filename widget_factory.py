from widget_loader import WidgetLoader
from dit_flow.config_translator import ConfigTranslator
from dit_flow.flow_widget import create_widget_class

class WidgetFactory:
    '''
    Abstract class encapsulating generation of widgets
    '''

    factories = {}
    loader = WidgetLoader()
    config_loader = ConfigTranslator()


    @staticmethod
    def set_config_file(config_file):
        WidgetFactory.config_loader.set_config_file(config_file)

    @staticmethod
    def add_factory(id, widgetFactory):
        WidgetFactory.factories.put[id] = widgetFactory

    @staticmethod
    def has_factory(id):
        return id in WidgetFactory.factories.keys()

    @staticmethod
    def create_widget(id):
        if not WidgetFactory.has_factory(id):
            widget_class = create_widget_class(id, WidgetFactory.loader)
            WidgetFactory.add_factory(id, widget_class)
        return WidgetFactory.factories[id].create()
