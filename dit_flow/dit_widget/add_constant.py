#!/usr/bin/python
"""Adds a constant to all numeric values in a column file."""
import csv

from circuits import Component
from dit_flow.dit_widget.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType


class AddConstant(Component, FlowWidget):

    channel = 'add_constant'

    metadata = {
        FlowWidget.name_key: 'AddConstant', # component name in format that can be used in graphs
        FlowWidget.description_key: 'Adds constant to all values in infile and writes the result to ' \
                                    'outfile',
        FlowWidget.inputs_key: [ # list of input ports
            ('infile', PortType.STR),
            ('outfile', PortType.STR),
            ('logfile', PortType.STR),
            ('constant', PortType.INT)
        ],
        FlowWidget.outputs_key: [ # list of output ports
            ('outfile', PortType.STR),
            ('logfile', PortType.STR),
        ]
    }

    def go(self, *args, **kwargs):
        print("Received args: ", args, kwargs)
        result = add_constant(*args)
        print('result: ', result)
        return result


def add_constant(infile, outfile, constant, logfile):
    # Adds constant to all values in infile and writes the result to
    # outfile.
    with open(infile, newline='') as _in, \
         open(outfile, 'w', newline='') as _out, \
         open(logfile, 'a') as _log:
        print('Adding {} to the column'.format(constant), file=_log)
        data = csv.reader(_in, )
        output = csv.writer(_out)
        for line in _in:
            for item in line:
                if (float(item) not in [-10]): #d.missing_values):
                    value = float(item) + constant

    return [outfile, logfile]
