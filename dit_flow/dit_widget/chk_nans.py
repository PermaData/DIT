#!/usr/bin/python
"""checks if value is text rather than a number."""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def chk_nans(print_flag, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # checks if numerical value is not a number, but rather text.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Find values that are not numbers')
            if print_flag:
                logger.info('{:>10}{:>20}'.format('Record', 'Value'))
            reader = csv.reader(_in)
            for line in reader:
                for item in line:
                    record = record + 1
                    flag = is_float(item)
                    if not flag:
                        count = count + 1
                        if print_flag:
                            logger.info('{:10.0f}{:>20}'.format(float(record), item))
            logger.info('\tTotal number ={}'.format(count))


def is_float(data):
    try:
        float(data)
        return True
    except ValueError:
        return False


def parse_arguments():
    parser = ap.ArgumentParser(description="checks if value is text rather than a number.")

    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_nans(args.print_flag,
             args.input_data_file, args.output_data_file, args.log_file)
