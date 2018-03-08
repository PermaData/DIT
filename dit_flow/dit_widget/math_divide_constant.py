#!/usr/bin/python
"""Divides all numeric values in a column file by a constant."""
import argparse as ap
import csv
from array import array
from decimal import *

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def is_number(s):  # checks if the item in list is a number
    try:
        float(s)
        return True
    except ValueError:
        return False


def math_divide_constant(constant, missing_value, input_data_file=None,
                         output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Divides all values in input_data_file by a constant and writes result to
    # output_data_file.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    NaN_toggle = True
    NaN_count = 0
    record = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Dividing column by {}'.format(constant))
            output = csv.writer(_out)
            reader = csv.reader(_in)
            getcontext().prec = 2
            for line in reader:
                # note: if this is an array of floats, the values get approximated when appended.
                # Making it an array of decimals avoids this problem.
                new_line = array('d')
                for item in line:
                    record = record + 1
                    if is_number(item):
                        if float(item) != float(missing_value):
                            value = Decimal(float(item) / constant)
                        else:
                            value = missing_value
                        new_line.append(value)
                    else:
                        NaN_count = NaN_count + 1
                        if NaN_toggle: # print the legend only once, but only if needed
                            logger.info('    Records with non-number entry types:'\
                                        '\n{:>15} {:>20}'.format('Record', 'Value'))
                            NaN_toggle = False
                        logger.info('{:15.0f} {:>20}'.format(float(record), item))
                        new_line.append(missing_value)
                output.writerow(['{0:.2f}'.format(x) for x in new_line])
            logger.info('    Total number of non-number entries: {}'.format(NaN_count))


def parse_arguments():
    parser = ap.ArgumentParser(description="Divides all values in "
                               "input_data_file and writes the result to "
                               "output_data_file.")

    parser.add_argument('constant', type=float, help='Constant to divide column values.')
    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    math_divide_constant(args.constant, args.missing_value,
                         args.input_data_file, args.output_data_file, args.log_file)
