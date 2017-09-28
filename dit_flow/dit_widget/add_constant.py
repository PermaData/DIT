#!/usr/bin/python
"""Adds a constant to all numeric values in a column file."""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.setup_logger import setup_logger

def add_constant(constant, missing_value, input_data_file=None, output_data_file=None, log_file=None):
    # Adds constant to all values in input_data_file and writes the result to
    # output_data_file.
    logger = setup_logger(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values to be added to is required.'
    assert output_data_file is not None, 'An output CSV file to write new values to is required.'
    with open(input_data_file, newline='') as _in, \
         open(output_data_file, 'w', newline='') as _out:
        logger.info('Adding {} to the column'.format(constant))
        output = csv.writer(_out, quotechar="'", quoting=csv.QUOTE_ALL)
        reader = csv.reader(_in, quotechar="'")
        for line in reader:
            new_line = array('f')
            for item in line:
                if float(item) != float(missing_value):
                    value = float(item) + float(constant)
                else:
                    value = float(missing_value)
                new_line.append(value)
            output.writerow(['{:.2f}'.format(x) for x in new_line])

def parse_arguments():
    parser = ap.ArgumentParser(description="Adds constant to all values in " \
                               "input_data_file and writes the result to " \
                               "output_data_file.")

    parser.add_argument('constant', type=float, help='Constant to be added to the column values.')
    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    add_constant(args.constant, args.missing_value,
                 args.input_data_file, args.output_data_file, args.log_file)
