import csv

from dit_flow.utility_widget import UtilityWidget
from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


class VariableMap(UtilityWidget):

    def __init__(self, *args, **kwargs):
        super(VariableMap, self).__init__(*args, **kwargs)
        self.widget_method = self.variable_map

    def variable_map(self, input_data, map_file, log_file=None, log_level=DEFAULT_LOG_LEVEL):
        # reads in a file mapping input columns to output columns
        # then copies the input data to the output data

        logger = setup_logger(__name__, log_file, log_level=log_level)
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

        # read in all the variable mapping information
        col_number = []
        in_name = []
        operation = []
        out_name = []
        in_index = []
        out_index = []
        units = []
        description = []
        num_rec = 0
        in_column = 0
        out_column = 0
        with open(map_file, newline='') as _in:
#            logger.info('\tRead Variable Mapping File')
            logger.info('\tMap file: {m}'.format(m=map_file))
            reader = csv.reader(_in)
            # Possible improvement: skip over n "headlines" instead of just 1
            firstline = True
            for line in reader:
#                logger.info('{}'.format(line))
                if (firstline):
                    # skips first line
                    firstline = False
                    continue
                # Divide each line into entries
                num_rec = num_rec + 1
                col_number.append(line[0])
                in_name.append(line[1])
                operation.append(line[2])
                out_name.append(line[3])
                in_index.append(line[4])
                out_index.append(line[5])
                units.append(line[6])
                description.append(line[7])

# Create mapping files
        headline = []
        for i in range(num_rec):
#            logger.info('record: {}'.format(i))
            if (in_index[i] != '0'):
                in_column = in_column + 1
                    # If the input exists, store data about it
                in_map.update({in_name[i]: int(in_index[i]) - 1})
                in_details.update({in_name[i]: [operation[i], description[i]]})
            if (out_index[i] != '0'):
                out_column = out_column + 1
                    # If the output exists, store data about it
                out_map.update({out_name[i]: int(out_index[i]) - 1})
                out_details.update({out_name[i]: [units[i], description[i]]})
                name_converter[in_name[i]] = out_name[i]
                text_string = ('{} ({})'.format(out_name[i], units[i]))
                headline.append(text_string)
#        logger.info('in col: {} out col: {}'.format(in_column, out_column))

# define output data
        output_data = []

# append header of output data
        output_data.append(headline)

# Figure out which columns need to be copied
        num_copies = 0
        copy_from = []
        copy_to = []
        for i in range(num_rec):
            if (operation[i] == 'copy'):
                num_copies = num_copies + 1
                copy_from.append(int(in_index[i]) - 1)
                copy_to.append(int(out_index[i]) - 1)
#                logger.info('from: {} to: {}'.format(copy_from[i],copy_to[i]))
        logger.info('\tnum_copies: {} '.format(num_copies))

# copy input data to output data
        firstline = True
        for line in input_data:
            # Copy selected columns
            if (firstline):
                firstline = False
                continue
            outputline = [''] * out_column
            for i in range(num_copies):
                outputline[copy_to[i]] = line[copy_from[i]]
            output_data.append(outputline)

# return to DIT
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
