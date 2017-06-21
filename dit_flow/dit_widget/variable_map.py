import itertools
import csv
import re

from circuits import Component
from dit_flow.dit_widget.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType

class VariableMap(Component, FlowWidget):

    channel = 'variable_map'

    metadata = {
            FlowWidget.name_key: 'variable_map',
            FlowWidget.description_key: 'Provides input/output CSV file mapping.',
            FlowWidget.inputs_key: [
                    ('filename', PortType.STR),
                    ('mapfile', PortType.STR),
                    ('logfile', PortType.STR)
                ],
            FlowWidget.outputs_key: [
                #   - the name of the input csv.
                #   - the name of the output csv.
                #   - a dictionary of column name -> index for the input csv
                #   - a dictionary of column name -> index for the output csv
                #   - a dictionary of data column name -> destination column name
                ('IN', PortType.STR),
                ('OUT', PortType.STR),
                ('STEP', PortType.STR),
                ('INMAP', PortType.STR),
                ('OUTMAP', PortType.STR),
                ('CROSSMAP', PortType.DICT),
                ('LOGFILE_OUT', PortType.STR)
            ]
        }

    def go(self, *args, **kwargs):
        print(self.channel, ' received go event')
        result = variable_map(*args)
        return result

def variable_map(filename, mapfile, logfile):
    # Columns are separated by whitespace
    sep = '  '
    n_entries = 7

    print('variable_map args: ', filename, '  ', mapfile, '  ', logfile)
    # in_map = {column name: column index} of the original data file
    # in_details: {column name: [units, description]} of the original data file
    # out_map = {column name: column index} of the processed file
    # out_details: {column name: [units, description]} of the processed file
    # name_converter: {input column name: output column name}
    in_map = {}
    in_details = {}
    out_map = {}
    out_details = {}
    name_converter = {}
    with open(mapfile) as f:
        # Possible improvement: skip over n "headlines" instead of just 1
        firstline = True
        for line in f:
            if (firstline):
                # skips first line
                firstline = False
                continue
            # Divide each line into entries
            pattern = '{0}+'.format(sep)
            entries = re.split(pattern, line)
            if (len(entries) != n_entries and len(entries) != 0):
                # Check that the number of entries is correct
                with open(logfile, 'a') as log:
                    print('Map file: {m}'.format(m=mapfile), file=log)
                    print('Expected number of columns: {e}'.format(e=n_entries), file=log)
                    print('Read number of columns: {r}'.format(r=len(entries)), file=log)
                    print('Read entries: ', entries, sep=' ', file=log)
                raise IndexError('File has the wrong number of columns.')
            else:
                in_header, operation, out_header, in_index, out_index, \
                    units, description = entries_breakout(entries)
                # TODO: description and units should be passed around as metadata
                # Build the name converter
                name_converter[in_header] = out_header
                if (in_header and in_index > 0):
                    # If the input exists, store data about it
                    in_map.update({in_header: in_index-1})
                    in_details.update({in_header: [operation, description]})
                if (out_header and out_index > 0):
                    # If the output exists, store data about it
                    out_map.update({out_header: out_index-1})
                    out_details.update({out_header: [units, description]})

    with open(filename, newline='') as _in, \
         open(convert_to_out(filename), 'w', 0o666, newline='') as _out:
        data = csv.reader(_in)
        output = csv.writer(_out)
        # headline = next(data)  # Pulls the first line of the file as headers
        # Construct the first line of the output file from the given information
        headline = [''] * len(out_map)
        for name, index, details in zip(out_map.keys(), out_map.values(),
                                        out_details.values()):
            if (details[0]):
                # units exist
                formatstr = '{name} ({unit})'
            else:
                formatstr = '{name}'
            headline[index] = formatstr.format(name=name, unit=details[0])
        # print(headline)
        output.writerow(headline)
        copies = {}
        for in_name in in_map.keys():
            # Figure out which columns need to be copied
            if name_converter[in_name] in out_map:
                # copies is a dictionary of input column index -> output column index
                copies[in_map[in_name]] = out_map[name_converter[in_name]]
        firstline = True
        for line in data:
            # Copy selected columns
            if (firstline):
                firstline = False
                continue
            outputline = [''] * len(out_map)
            for _from, _to in copies.items():
                outputline[_to] = line[_from]
            output.writerow(outputline)

    # Returns:
    #   - the name of the input csv.
    #   - the name of the output csv.
    #   - a dictionary of column name -> index for the input csv
    #   - a dictionary of column name -> index for the output csv
    #   - a dictionary of data column name -> destination column name
    result = [filename,
              convert_to_out(filename),
              in_map,
              out_map,
              {v: k for k, v in name_converter.items()},
              logfile]

    return result

def convert_to_out(infile_name):
    outfile_name = infile_name.replace('In', 'Out')
    return outfile_name
    # return re.sub('([_/])In[_/]', lambda m: '{0}Out{0}'.format(m.groups(1)),
    #               infile_name)


def entries_breakout(entries):
    quotechar = "'"
    in_header = entries[0].strip(quotechar)
    operation = entries[1].strip(quotechar)
    out_header = entries[2].strip(quotechar)
    in_index = int(entries[3])
    out_index = int(entries[4])
    units = entries[5].strip(quotechar)
    description = entries[6].strip(quotechar)
    return in_header, operation, out_header, in_index, out_index, units, description
