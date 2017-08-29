import os

from circuits import Component
from dit_flow.dit_widget.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType


class FileManager(Component, FlowWidget):

    channel = 'file_manager'

    metadata = {
        FlowWidget.name_key: 'FileManager', # component name in format that can be used in graphs
        FlowWidget.description_key: 'Loops through input files and creates flow unique filenames for each ' \
                       'step in the flow', # (optional) textual description on what the component does
        # icon: (optional): visual icon for the component, matching icon names in Font Awesome
        FlowWidget.inputs_key: [ # list of input ports
            ('FILENAMES', PortType.ARRAY)
            ],
        FlowWidget.outputs_key: [ # list of output ports
                ('CURRENT', PortType.ARRAY),
                ('FID', PortType.INT),
                ('LOGFILE', PortType.STR)
            ]
    }

    def go(self, *args, **kwargs):
        result = file_manager(*args)
        return result

def file_manager(FILENAMES):
    """
    FILENAMES: a sequence of paths to data files
    CURRENT: sends out a sequence of filenames after confirming they exist
    FID: a sequential numeric identifier for each file
    LOGFILE: sends out a sequence of log filenames that correspond to a data file
    """
    print("inside file_manager, filenames: ", FILENAMES)
    step_files = []
    for identifier, name in enumerate(FILENAMES):
        path, fname = name.rsplit('/', 1)
        log_name = '{pth}/{name}.log'.format(pth=path, name=fname)
        try:
            # Open the file. If the file doesn't exist, the error will be
            # caught.
            f = open(name, 'r')
            f.close()
            # Create/clear the log file
            open(log_name, 'w').close()
            os.chmod(log_name, 0o666)
            step_files.append((name, identifier + 1, log_name))
        except FileNotFoundError:
            with open(log_name, 'w') as log:
                print('The file {f} was not found.'.format(f=name), file=log)
                os.chmod(log_name, 0o666)
    return step_files
