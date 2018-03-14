#!/usr/bin/python
"""Copy column and multiply by constant (out = in * constant)"""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def calc_copy_col_mult_const(constant, missing_value, input_data_file=None, output_data_file=None, log_file=None):
# out = in * constant
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Copy column and multiply by constant (out = in * constant)')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                new_line = array('f')
                for item in line:
                    if (float(item) != float(missing_value)):
                        value = float(item) * float(constant)
                    else:
                        value = float(missing_value)
                    new_line.append(value)
                output.writerow(['{:.8f}'.format(x) for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description='Multiply two columns (out = column_a * column_b).')

    parser.add_argument('constant', type=float, help='constant to multiply')
    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_copy_col_mult_const(args.constant, args.missing_value, args.input_data_file,
                      args.output_data_file, args.log_file)
