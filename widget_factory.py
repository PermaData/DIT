import imp
import re
import yaml
from stringcase import pascalcase
from widget_loader import WidgetLoader
from dit_flow.config_translator import ConfigTranslator
from dit_flow.reader_widget import ReaderWidget
from dit_flow.manipulation_widget import ManipulationWidget
from dit_flow.writer_widget import WriterWidget

class WidgetCreateException(Exception):
    pass

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
        WidgetFactory.factories[id] = widgetFactory

    @staticmethod
    def has_factory(id):
        return id in WidgetFactory.factories.keys()

    @staticmethod
    def create_widget(id):
        if not WidgetFactory.has_factory(id):
            widget_class = create_widget_class(id, WidgetFactory.loader)
            WidgetFactory.add_factory(id, widget_class)
        return WidgetFactory.factories[id]()

def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)

def inputs_from_config(config_file):
    inputs = []
    input_regex = re.compile('input_\d+$')
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
    for name, value in override_yaml.items():
        if None != input_regex.match(name):
            inputs.append((value, override_yaml[name + '_type']))
    return inputs

def type_from_config(config_file):
    base_class = None
    try:
        with open(config_file, 'r') as cfile:
            override_yaml = yaml.safe_load(cfile)
        the_type = pascalcase(override_yaml['type'])
        if the_type == 'ManipulationWidget':
            base_class = ManipulationWidget
        elif the_type == 'ReaderWidget':
            base_class = ReaderWidget
        elif the_type == 'WriterWidget':
            base_class = WriterWidget
        else:
            raise WidgetCreateException('Do not know how to make a {} widget'.format(the_type))
    except TypeError as te:
        raise WidgetCreateException('Cannot open widget config: {}'.format(config_file))

    return base_class

def description_from_config(config_file):
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
        description = override_yaml['description']
    return description

def method_from_config(id, method_file):
    modes = imp.get_suffixes()
    the_module = None
    with open(method_file) as open_mf:
        the_module = imp.load_module('{}.{}'.format(id, id), open_mf, '{}.py'.format(id), modes[-2])
    return getattr(the_module, id)

def create_widget_class(id, loader):
    (config_path, method_path) = loader.find_widget(id)
    base_class = type_from_config(config_path)
    description = description_from_config(config_path)
    inputs = inputs_from_config(config_path)
    widget_method = method_from_config(id, method_path)
    typing = type(pascalcase(id),
                  (base_class,),
                  {
                      "__init__": __init__,
                      "description": description,
                      "inputs": inputs,
                      "widget_method": widget_method})
    return typing
