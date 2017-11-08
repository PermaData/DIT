#!/usr/bin/python
"""Copy input column to output column"""
import argparse as ap
import csv

from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


def calc_copy_col(input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # output = in_column_A + in_column_B
    logger = setup_logger(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Copy input column to output column')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                output.writerow(line)


def parse_arguments():
    parser = ap.ArgumentParser(description='Copy input column to output column.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_copy_col(args.input_data_file, args.output_data_file, args.log_file)
