import imp
import re
import yaml

from stringcase import pascalcase
from dit_flow.constants import WIDGET_TYPES
from widget_loader import WidgetLoader
from dit_flow.dit_widget.common.setup_logger import DEFAULT_LOG_LEVEL
from dit_flow.reader_widget import ReaderWidget
from dit_flow.manipulation_widget import ManipulationWidget
from dit_flow.writer_widget import WriterWidget
from dit_flow.utility_widget import UtilityWidget


class WidgetCreateException(Exception):
    pass


class WidgetFactory:
    '''
    Abstract class encapsulating generation of widgets
    '''

    factories = {}
    loader = WidgetLoader()

    @staticmethod
    def add_factory(id, widgetFactory):
        WidgetFactory.factories[id] = widgetFactory

    @staticmethod
    def has_factory(id):
        return id in WidgetFactory.factories.keys()

    @staticmethod
    def create_widget(id, log_file=None, log_level=DEFAULT_LOG_LEVEL):
        if not WidgetFactory.has_factory(id):
            widget_class = create_widget_class(id, WidgetFactory.loader)
            WidgetFactory.add_factory(id, widget_class)
        new_widget = WidgetFactory.factories[id](log_file=log_file, log_level=log_level)
        if not isinstance(new_widget, UtilityWidget):
            new_widget.widget_method = method_from_config(id, new_widget.method_path)
        return new_widget


def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)


def widget_configs_by_type(loader):
    widget_lists = {}
    config_list = loader.find_all_widget_configs()
    widget_lists[WIDGET_TYPES.READER_WIDGET.value] = reader_widget_configs(config_list)
    widget_lists[WIDGET_TYPES.WRITER_WIDGET.value] = writer_widget_configs(config_list)
    widget_lists[WIDGET_TYPES.MANIPULATION_WIDGET.value] = manipulation_widget_configs(config_list)
    return widget_lists


def reader_widget_configs(all_configs):
    reader_configs = []
    for config in all_configs:
        if type_name_from_config(config) == WIDGET_TYPES.READER_WIDGET.value:
            with open(config, 'r') as cfile:
                config_yaml = yaml.safe_load(cfile)
            config_yaml['name'] = widget_name_from_config(config)
            reader_configs.append(config_yaml)
    return reader_configs


def writer_widget_configs(all_configs):
    writer_configs = []
    for config in all_configs:
        if type_name_from_config(config) == WIDGET_TYPES.WRITER_WIDGET.value:
            with open(config, 'r') as cfile:
                config_yaml = yaml.safe_load(cfile)
            config_yaml['name'] = widget_name_from_config(config)
            writer_configs.append(config_yaml)
    return writer_configs


def manipulation_widget_configs(all_configs):
    manipulation_configs = []
    for config in all_configs:
        if type_name_from_config(config) == WIDGET_TYPES.MANIPULATION_WIDGET.value:
            with open(config, 'r') as cfile:
                config_yaml = yaml.safe_load(cfile)
            config_yaml['name'] = widget_name_from_config(config)
            manipulation_configs.append(config_yaml)
    return manipulation_configs


def widget_name_from_config(config_file):
    return config_file.name.replace('.yaml', '')


def inputs_from_config(config_file):
    inputs = []
    input_regex = re.compile('input_\d+$')
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
    for name, value in override_yaml.items():
        if input_regex.match(name) is not None:
            inputs.append((value, override_yaml[name + '_type']))
    return inputs


def type_name_from_config(config_file):
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
    the_type = pascalcase(override_yaml['type'])
    return the_type


def type_from_config(config_file):
    base_class = None
    try:
        the_type = type_name_from_config(config_file)
        if the_type == WIDGET_TYPES.MANIPULATION_WIDGET.value:
            base_class = ManipulationWidget
        elif the_type == WIDGET_TYPES.READER_WIDGET.value:
            base_class = ReaderWidget
        elif the_type == WIDGET_TYPES.WRITER_WIDGET.value:
            base_class = WriterWidget
        elif the_type == WIDGET_TYPES.UTILITY_WIDGET.value:
            base_class = UtilityWidget
        else:
            raise WidgetCreateException('Do not know how to make a {} widget'.format(the_type))
    except TypeError:
        raise WidgetCreateException('Cannot open widget config: {}'.format(config_file))

    return base_class


def description_from_config(config_file):
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
        description = override_yaml['description']
    return description


def class_from_config(id, method_file):
    modes = imp.get_suffixes()
    with open(method_file) as open_mf:
        the_module = imp.load_module('{}.{}'.format(id, id), open_mf, '{}.py'.format(id), modes[-2])
    return getattr(the_module, pascalcase(id))


def method_from_config(id, method_file):
    modes = imp.get_suffixes()
    with open(method_file) as open_mf:
        the_module = imp.load_module('{}.{}'.format(id, id), open_mf, '{}.py'.format(id), modes[-2])
    return getattr(the_module, id)


def create_widget_class(id, loader):
    (config_path, method_path) = loader.find_widget(id)
    base_class = type_from_config(config_path)
    if base_class == UtilityWidget:
        typing = class_from_config(id, method_path)
    else:
        description = description_from_config(config_path)
        inputs = inputs_from_config(config_path)
        typing = type(pascalcase(id),
                      (base_class,),
                      {
                          "__init__": __init__,
                          "description": description,
                          "inputs": inputs,
                          "method_path": method_path
                      })
    return typing
