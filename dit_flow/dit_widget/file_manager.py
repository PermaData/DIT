import os

from circuits import Component
from port import PortType


class FileManager(Component):

    channel = 'file_manager'

    metadata = {
        'widget_name': 'FileManager', # component name in format that can be used in graphs
        'description': 'Loops through input files and creates flow unique filenames for each ' \
                       'step in the flow', # (optional) textual description on what the component does
        # icon: (optional): visual icon for the component, matching icon names in Font Awesome
        'inPorts': { # list of input ports
                'FILENAMES': PortType.ARRAY
            },
        'outPorts': { # list of output ports
                'CURRENT': PortType.ARRAY,
                'FID': PortType.INT,
                'LOGFILE': PortType.STR
            }
    }

    def get_metadata(self):
        return metadata

    def get_name(self):
        return self.metadata['widget_name']

    def get_description(self):
        return self.metadata['description']

    def get_input_ports(self):
        return self.metadata['inPorts']

    def get_output_ports(self):
        return self.metadata['outPorts']

    def go(self, *args, **kwargs):
        print("Received args: ", args, kwargs)
        result = file_manager(*args)
        print('result: ', result)
        return result

    def la(self, *args, **kwargs):
        print('Received la event...')
        return 'success!!'

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
        print("identifier: ", identifier, "  name: ", name)
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
