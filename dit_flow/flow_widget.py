import imp
import re
import yaml
from stringcase import pascalcase
from collections import OrderedDict
from dit_flow.dit_widget.port import PortType

class FlowWidget(object):

    channel = 'flow_widget'
    description = None
    required_args = {'input_data_file': '', 'output_data_file': '', 'log_file': ''}
    required_arg_types = {'input_data_file': PortType.STR,
                          'output_data_file': PortType.STR,
                          'log_file': PortType.STR}
    input_args = OrderedDict()
    input_arg_types = OrderedDict()
    widget_method = None

    def __init__(self, classtype):
        self._type = classtype

    def speak(self):
        print("I say: ", self.channel)

    def go(self):
        print(self.channel, ' received go event')
        result = self.widget_method(*self.input_args, **self.required_args)
        return result

def inputs_from_config(config_file):
    inputs = []
    input_regex = re.compile('input_\d+$')
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
    print(input_regex)
    for name, value in override_yaml.items():
        if None != input_regex.match(name):
            inputs.append((value, override_yaml[name + '_type']))
    return inputs

def type_from_config(config_file):
    with open(config_file, 'r') as cfile:
        override_yaml = yaml.safe_load(cfile)
    base_class = pascalcase(override_yaml['type'])
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
    widget_method = method_from_config(method_path)
    return type(pascalcase(id),
                (base_class),
                {
                    "__init__": __init__,
                    "description": description,
                    "inputs": inputs,
                    "widget_method": widget_method})
