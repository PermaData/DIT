#!/usr/bin/python
"""Replaces one number with another in a column."""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message

def replace_num_equal(criteria, constant, print, input_data_file=None, output_data_file=None, log_file=None):
    # Replaces values = criteria in input_data_file and writes the result to
    # output_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
        open(output_data_file, 'w', newline='') as _out:
        logger.info('Replacing {} with {}'.format(criteria,constant))
        if print:
            logger.info('{:>10} {:>20} {:>20}'.format('Record','Old Value','New Value'))
        output = csv.writer(_out)
        reader = csv.reader(_in)
        for line in reader:
            new_line = array('f')
            for item in line:
                record = record + 1
                if float(item) == float(criteria):
                    if print:
                        logger.info('{:10.0f} {:>20} {:>20}'.format(float(record),item,constant))
                    value = float(constant)
                    count = count +1
                else:
                    value = float(item)
                new_line.append(value)
            output.writerow(['{:.2f}'.format(x) for x in new_line])
        logger.info('\n\t Total number ={}'.format(count))

def parse_arguments():
    parser = ap.ArgumentParser(description="Replaces values = criteria in " \
                               "input_data_file and writes the result to " \
                               "output_data_file.")

    parser.add_argument('criteria', type=float, help='Value to replace.')
    parser.add_argument('constant', type=float, help='Replacement value.')
    parser.add_argument('print', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    replace_num_equal(args.criteria,args.constant, 
                 args.input_data_file, args.output_data_file, args.log_file)
