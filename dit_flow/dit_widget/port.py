from enum import Enum
from circuits import Component

class PortType(Enum):
    INT = 1
    REAL = 2
    STR = 3
    ARRAY = 4

class Port(Component):
    """
    FBP style port with:
    addressable: boolean telling whether the port is an ArrayPort
    port_name: port name
    port_type: port datatype, for example boolean
    required: boolean telling whether the port needs to be connected for the component to work
    description: textual description of the port
    """

    def _init(self, port_name, port_type=PortType.STR, addressable=False, required=False,
            description='Either input or output argument for flow or widget'):
        self.port_name = port_name
        self.port_type = port_type
        self.addressable = addressable
        self.required = required

