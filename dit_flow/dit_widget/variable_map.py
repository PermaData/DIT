import csv
import re

from dit_flow.utility_widget import UtilityWidget
from dit_flow.dit_widget.common.setup_logger import setup_logger


class VariableMap(UtilityWidget):

    def __init__(self, *args, **kwargs):
        super(VariableMap, self).__init__(*args, **kwargs)
        self.widget_method = self.variable_map

    def variable_map(self, input_data, map_file, log_file=None):
        # Columns are separated by whitespace
        sep = '  '
        n_entries = 7

        logger = setup_logger(__name__, log_file)
        logger.info('Running variable mapper.')
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
        with open(map_file) as f:
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
                    logger.info('Map file: {m}'.format(m=map_file))
                    logger.info('Expected number of columns: {e}'.format(e=n_entries))
                    logger.info('Read number of columns: {r}'.format(r=len(entries)))
                    logger.info('Read entries: ', entries, sep=' ')
                    raise IndexError('File has the wrong number of columns.')
                else:
                    in_header, operation, out_header, in_index, out_index, \
                        units, description = self.entries_breakout(entries)
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

        output_data = []
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
        output_data.append(headline)
        copies = {}
        for in_name in in_map.keys():
            # Figure out which columns need to be copied
            if name_converter[in_name] in out_map:
                # copies is a dictionary of input column index -> output column index
                copies[in_map[in_name]] = out_map[name_converter[in_name]]
        firstline = True
        for line in input_data:
            # Copy selected columns
            if (firstline):
                firstline = False
                continue
            outputline = [''] * len(out_map)
            for _from, _to in copies.items():
                outputline[_to] = line[_from]
            output_data.append(outputline)

        # Returns:
        #   - the output data.
        #   - a dictionary of column name -> index for the input csv
        #   - a dictionary of column name -> index for the output csv
        #   - a dictionary of data column name -> destination column name
        result = [output_data,
                  in_map,
                  out_map,
                  {v: k for k, v in name_converter.items()}]

        return result


    def entries_breakout(self, entries):
        quotechar = "'"
        in_header = entries[0].strip(quotechar)
        operation = entries[1].strip(quotechar)
        out_header = entries[2].strip(quotechar)
        in_index = int(entries[3])
        out_index = int(entries[4])
        units = entries[5].strip(quotechar)
        description = entries[6].strip(quotechar)
        return in_header, operation, out_header, in_index, out_index, units, description
