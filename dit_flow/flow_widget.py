import yaml
import sys

from circuits import Component

class FlowWidget(object, Component):

    channel = 'flow_widget'

    def speak(self):
        print("I say: ", self.channel)


    def read_config(self, config_file):
        override_yaml = yaml.load(open(config_file, 'r'))
        this_module = sys.modules[__name__]
        for name, value in override_yaml.items():
            # log.info('overriding nasateam constant:{}:{}=>{}'.format(
            print('overriding nasateam constant:{}:{}=>{}'.format(
                name, self.getattr(this_module, name), value))
            self.setattr(this_module, name, value)


    @property
    def metadata(self):
        return self._metadata

    @property
    def name(self):
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def input_args(self):
        if type(self._input_args) is not list:
            print('Please set the input_args of class {} to a list of the
                input arguments for the function called in the form:
                [(arg_1, PortType), (arg_2, PortType), etc.]').format(self.name)
        return self._input_args

    @property
    def output_args(self):
        if type(self._output_args) is not list:
            print('Please set the output_args of class {} to a list of the
                return arguments for the function called in the form:
                [(arg_1, PortType), (arg_2, PortType), etc.]').format(self.name)
        return self._output_args

    @property
    def input_arg_names(self):
        if self._intput_arg_names is None:
            self._input_args_names = [arg[0] for arg in self.input_args]
        return self._input_arg_names

    @property
    def output_arg_names(self):
        if self._output_arg_names is None:
            self._output_args_names = [arg[0] for arg in self.output_args]
        return self._output_arg_names

    @property
    def input_arg_values(self):
        if self._input_arg_values is None:
            self._input_arg_values = {arg: None for arg in self.input_arg_names}
        return self._input_arg_values

    @input_arg_values.setter
    def input_arg_values(self, new_values):
        self._input_arg_values = new_values

    def are_input_args_full(self):
        return reduce((lambda arg: arg is None), self.input_arg_values)

    @property
    def output_arg_values(self):
        if self._output_arg_values is None:
            self._output_arg_values = {arg: None for arg in self.output_arg_names}
        return self._output_arg_values

    @output_arg_values.setter
    def output_arg_values(self, new_values):
        self._output_arg_values = new_values

    def are_output_args_full(self):
        return reduce((lambda arg: arg is None), self.output_arg_values)

    def go(self, *args, **kwargs):
        print(self.channel, ' received go event')
        result = read_file(*args)
        return result
