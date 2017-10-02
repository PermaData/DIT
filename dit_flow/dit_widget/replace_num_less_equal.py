#!/usr/bin/python
"""Replaces numbers less or equal to than criteria with constant in a column."""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message

def replace_num_less_equal(criteria, constant, input_data_file=None, output_data_file=None, log_file=None):
    # Replaces values <= criteria with constant in input_data_file and writes result to
    # output_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
         open(output_data_file, 'w', newline='') as _out:
        logger.info('Replacing <={} with {}'.format(criteria,constant))
        output = csv.writer(_out)
        reader = csv.reader(_in)
        for line in reader:
            new_line = array('f')
            for item in line:
                record = record + 1
                if float(item) <= float(criteria):
                    value = float(constant)
                    count = count + 1
                else:
                    value = float(item)
                new_line.append(value)
            output.writerow(['{:.2f}'.format(x) for x in new_line])
        logger.info('\n\t Total number ={}'.format(count))

def parse_arguments():
    parser = ap.ArgumentParser(description="Replaces values <= criteria in " \
                               "input_data_file and writes the result to " \
                               "output_data_file.")

    parser.add_argument('criteria', type=float, help='Value to replace.')
    parser.add_argument('constant', type=float, help='Replacement value.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    replace_num_less_equal(args.criteria,args.constant, 
                 args.input_data_file, args.output_data_file, args.log_file)
