from abc import ABCMeta, abstractmethod

class FlowWidget(metaclass=ABCMeta):
    name_key = 'widget_name'
    description_key = 'description'
    icon_key = 'icon'
    inputs_key = 'inargs'
    outputs_key = 'outargs'

    _metadata = {
            self.name_key}

    def init(self, name, ):
        self._metadata = None
        self._name = None
        self._description = None
        self._input_args = None
        self._output_args = None
        self._input_arg_names = None
        self._input_arg_values = None
        self._output_arg_names = None
        self._output_arg_values = None

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

    @abstractmethod
    def go(self, *args, **kwargs):
        pass
