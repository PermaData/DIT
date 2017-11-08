#!/usr/bin/python
"""Checks that all rows have the same number of columns"""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def chk_num_columns(print_flag, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Checks that all rows have the same number of columns.
    # assumes first row has correct number of columns.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Checking the number of columns')
            reader = csv.reader(_in)
            for i, line in enumerate(reader):
                record = record + 1
                if i == 0:
                    ref_num_column = 0
                    for j, item in enumerate(line):
                        ref_num_column = ref_num_column + 1
                    logger.info('\tCorrect number of columns: {:10.0f}'.format(float
                                                                               (ref_num_column)))
                    if print_flag:
                        logger.info('{:>10} {:>20}'.format('Record', 'Num Columns'))
                num_column = 0
                for j, item in enumerate(line):
                    num_column = num_column + 1
                if float(num_column) != float(ref_num_column):
                    count = count + 1
                    if print_flag:
                        logger.info('{:10.0f} {:>20} '.format(float(record), num_column))
            logger.info('\tTotal number rows with incorrect number columns={}'.format(count))


def parse_arguments():
    parser = ap.ArgumentParser(description="Checks that all rows have the same number of columns.")

    parser.add_argument('print_flag', type=bool, help='Printing value option.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_num_columns(args.print_flag,
                    args.input_data_file, args.output_data_file, args.log_file)
