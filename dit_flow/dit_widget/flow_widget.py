import os

from abc import abstractmethod
from circuits import Component
from port import PortType


class FileWidget(Component):

    metadata = {
        'widget_name': '', # component name in format that can be used in graphs
        'description': '', # (optional) textual description on what the component does
        'icon': '', # (optional): URL to visual icon for the component, matching icon names in Font Awesome
        'inPorts': { # list of input ports
                # e.g. 'FILENAMES': PortType.ARRAY
            },
        'outPorts': { # list of output ports
                # e.g. 'FID': PortType.INT,
            }
    }

    def get_metadata(self):
        return self.metadata

    def get_name(self):
        return self.metadata['widget_name']

    def get_description(self):
        return self.metadata['description']

    def get_input_ports(self):
        return self.metadata['inPorts']

    def get_output_ports(self):
        return self.metadata['outPorts']

    @abstractmethod
    def go(self, *args, **kwargs):
        pass
