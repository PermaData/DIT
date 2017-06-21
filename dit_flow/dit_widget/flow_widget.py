from abc import abstractmethod
class FlowWidget():
    name_key = 'widget_name'
    description_key = 'description'
    icon_key = 'icon'
    inputs_key = 'inPorts'
    outputs_key = 'outPorts'

    metadata = {}

    def get_metadata(self):
        return self.metadata

    def get_name(self):
        return self.metadata[self.name_key]

    def get_description(self):
        return self.metadata[self.description_key]

    def get_input_ports(self):
        return self.metadata[self.inputs_key]

    def get_output_ports(self):
        return self.metadata[self.outputs_key]

    def get_input_port_names(self):
        return [port[0] for port in self.metadata[self.inputs_key]]

    def get_output_port_names(self):
        return [port[0] for port in self.metadata[self.outputs_key]]

    def get_input_port_values(self):
        return [port[1] for port in self.metadata[self.inputs_key]]

    def get_output_port_values(self):
        return [port[1] for port in self.metadata[self.outputs_key]]

    @abstractmethod
    def go(self, *args, **kwargs):
        pass
