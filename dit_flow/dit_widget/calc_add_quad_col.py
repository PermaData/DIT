#!/usr/bin/python
"""Add two columns in quadrature (out = sqrt(column_a**2 +column_b**2))"""
import argparse as ap
import math
import csv
from array import array

from dit_flow.dit_widget.common.setup_logger import setup_logger


def calc_add_quad_col(missing_value, input_data_file=None, output_data_file=None, log_file=None):
    # output = in_column_A + in_column_B
    logger = setup_logger(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Add two columns in quadrature (out = sqrt(column_a**2 +column_b**2))')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                new_line = array('f')
                if (float(line[0]) != float(missing_value)) and (float(line[1])
                                                                 != float(missing_value)):
                    value = math.sqrt(float(line[0]) *
                                      float(line[0]) + float(line[1])*float(line[1]))
                else:
                    value = float(missing_value)
                new_line.append(value)
                output.writerow(['{:.10f}'.format(x) for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description='Add two columns \
                               in quadrature (out = sqrt(column_a**2 +column_b**2)).')

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_add_quad_col(args.missing_value, args.input_data_file,
                      args.output_data_file, args.log_file)
