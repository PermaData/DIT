import itertools
import csv
import re

import rill


@rill.component
@rill.inport('FILENAME')
@rill.inport('MAPFILE')
@rill.outport('IN')
@rill.outport('OUT')
@rill.outport('STEP')
@rill.outport('INMAP')
@rill.outport('OUTMAP')
def variable_map(FILENAME, MAPFILE, IN, OUT, STEP, INMAP, OUTMAP):
    # Columns are separated by whitespace
    sep = '  '
    n_entries = 7

    if (MAPFILE.upstream_count() == 1):
        # Use a single map file for all the files
        mapiter = itertools.repeat(MAPFILE.receive_once())
    else:
        # use different map files
        mapiter = MAPFILE.iter_contents()

    for Dname, Mname in zip(FILENAME.iter_contents(), mapiter):
        # Dname is the data file name
        # Mname is the map file name
        in_map = {}
        in_details = {}
        out_map = {}
        out_details = {}
        name_converter = {}
        with open(Mname) as f:
            firstline = True
            for line in f:
                if (firstline):
                    firstline = False
                    continue
                pattern = '{0}+'.format(sep)
                entries = re.split(pattern, line)
                if (len(entries) != n_entries and len(entries) != 0):
                    print(entries)
                    raise IndexError('File has the wrong number of columns.')
                else:
                    in_header, operation, out_header, in_index, out_index, \
                        units, description = entries_breakout(entries)
                    # TODO: description and units should be passed around as metadata
                    name_converter[in_header] = out_header
                    if (in_header and in_index):
                        in_map.update({in_header: in_index-1})
                        in_details.update({in_header: [operation, description]})
                    if (out_header and out_index):
                        out_map.update({out_header: out_index-1})
                        out_details.update({out_header: [units, description]})
        with open(Dname, newline='') as _in, open(convert_to_out(Dname), 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            # headline = next(data)  # Pulls the first line of the file as headers
            headline = [''] * len(out_map)
            for name, index, details in zip(out_map.keys(), out_map.values(),
                                            out_details.values()):
                if (details[0]):
                    formatstr = '{name} ({unit})'
                else:
                    formatstr = '{name}'
                headline[index-1] = formatstr.format(name=name, unit=details[0])
            # print(headline)
            # assert False
            output.writerow(headline)
            copies = {}
            for in_name in in_map.keys():
                # Figure out which items need to be copied
                if name_converter[in_name] in out_map:
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

        IN.send(Dname)
        OUT.send(convert_to_out(Dname))
        STEP.send(1)
        INMAP.send(in_map)
        OUTMAP.send(out_map)


def convert_to_out(infile_name):
    outfile_name = infile_name.replace('In', 'Out')
    return outfile_name
    # return re.sub('([_/])In[_/]', lambda m: '{0}Out{0}'.format(m.groups(1)),
    #               infile_name)


def entries_breakout(entries):
    in_header = entries[0]
    operation = entries[1]
    out_header = entries[2]
    in_index = int(entries[3])
    out_index = int(entries[4])
    units = entries[5]
    description = entries[6]
    return in_header, operation, out_header, in_index, out_index, units, description
