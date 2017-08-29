import csv
import os

from circuits import Component
from dit_flow.dit_widget.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType

class ReadFile(Component, FlowWidget):

    channel = 'read_file'

    metadata = {
            FlowWidget.name_key: 'read_file',
            FlowWidget.description_key: 'Provides input/output CSV file mapping.',
            FlowWidget.inputs_key: [
                ('name', PortType.STR),
                ('ID', PortType.INT),
                ('logfile', PortType.STR)
            ],
            FlowWidget.outputs_key: [
                ('main_name', PortType.STR),
                ('ID', PortType.STR),
                ('logfile', PortType.STR),
            ]
        }

    def go(self, *args, **kwargs):
        print(self.channel, ' received go event')
        result = read_file(*args)
        return result

def read_file(name, ID, logfile):
    print("args: ", name, "  ", ID, "  ", logfile)
    path, base = name.rsplit('/', 1)
    main_name = '{pth}/{ID}_In_{base}.csv'.format(pth=path, ID=ID,
                                                  base=base)
    with open(name, newline='') as _from, \
         open(main_name, 'w', 0o666, newline='') as _to:
        data = csv.reader(_from, quoting=csv.QUOTE_NONNUMERIC,
                          quotechar="'")
        try:
            isOK = column_check(data)
        except IOError as e:
            with open(logfile, 'a') as log:
                print(e, file=log)
            isOK = False
        _from.seek(0)
        output = csv.writer(_to, quoting=csv.QUOTE_NONNUMERIC,
                            quotechar="'")
        # Copies the data into the file that will be base input from now on
        for line in data:
            output.writerow(line)

    if (isOK):
        return [main_name, ID, logfile]
    else:
        return None


def column_check(data):
    # TODO: Check if this exhausts the iterator in containing scope
    # NOTE: It does, you need to reset with a seek(0) command
    # TODO: Pass in the log file so errors can be saved for later inspection
    """Expects a csv.reader object."""
    count = []
    for line in data:
        count.append(len(line))
    mean = round(float(sum(count)) / len(count))
    error = False
    for (i, item) in enumerate(count):
        if (item != mean):
            print('Line {0} has a different number of columns than the rest '
                  'of the file.'.format(i + 1))
            error = True
    if (error):
        raise IOError('One or more of the lines was flawed.')
    else:
        return True
