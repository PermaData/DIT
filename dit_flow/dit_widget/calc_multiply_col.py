#!/usr/bin/python
"""Multiply two columns (out = column_a * column_b)"""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def calc_multiply_col(missing_value, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # output = in_column_A + in_column_B
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Multiply two columns (out = column_a * column_b)')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                new_line = array('f')
                if (float(line[0]) != float(missing_value)) and (float(line[1])
                                                                 != float(missing_value)):
                    value = float(line[0]) * float(line[1])
                else:
                    value = float(missing_value)
                new_line.append(value)
                output.writerow(['{:.10f}'.format(x) for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description='Multiply two columns (out = column_a * column_b).')

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_multiply_col(args.missing_value, args.input_data_file,
                      args.output_data_file, args.log_file)
