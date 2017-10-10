#!/usr/bin/python
"""If column A < criteria set column B = constant."""
import argparse as ap
import csv
import numpy
import math
import statistics
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message

def cond_if_less(criteria, constant, print_flag, input_data_file=None, output_data_file=None, log_file=None):
# If column A < criteria in input_data_file column B = constant in output_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    with open(input_data_file, newline='') as _in, \
        open(output_data_file, 'w', newline='') as _out:
        logger.info('If column A < {} set column B = {}'.format(criteria,constant))
        if print_flag:
            logger.info('{:>10}{:>20}{:>20}{:>20}'.format('Record','Col A Value','Old Col B Value','New Col B Value'))
        output = csv.writer(_out)
        reader = csv.reader(_in)
        original_values = []

# transfer input values to local array
        for i, line in enumerate(reader):
            original_values.append([])
            for j, item in enumerate(line):
                original_values[i].append(item)

# perform conditional check
        record=0
        count=0
        for i, line in enumerate(original_values):
            new_line=[]
            record = record + 1
            col_a_value=line[0]
            for j, item in enumerate(line):
                old_col_b_value=item
            if (float(col_a_value) < float(criteria)):
                count=count+1
                new_line.append(col_a_value)
                new_line.append(constant)
                if print_flag:
                    logger.info('{:10.0f}{:>20}{:>20}{:>20}'.format(float(record),col_a_value,old_col_b_value,constant))
            else:
                for j, item in enumerate(line):
                    new_line.append(item)
            output.writerow(['{}'.format(x) for x in new_line])
        logger.info('\t Total number ={}'.format(count))

def parse_arguments():
    parser = ap.ArgumentParser(description="If column A < criteria in input_data_file column B = constant .")

    parser.add_argument('criteria', type=float, help='Value to run function on.')
    parser.add_argument('constant', type=float, help='Replacement value.')
    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    cond_if_less(args.criteria,args.constant, 
                 args.input_data_file, args.output_data_file, args.log_file)
