#!/usr/bin/python
"""Counts number of valid records in a column."""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def chk_count_valid_records_num(missing_value, input_data_file=None,
                                output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Counts number of valid records in input_data_file.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    count = 0
    record = 0
    with open(input_data_file, newline='') as _in:
        logger.info('Print valid values (not {})'.format(missing_value))
        logger.info('{:>10} {:>10} {:>10}'.format('Total', 'Valid', 'Percent'))
        reader = csv.reader(_in)
        for line in reader:
            for item in line:
                record = record + 1
                if float(item) != float(missing_value):
                    count = count + 1
        valid_fraction = float(count)/float(record)*100.
        logger.info('{:10.0f} {:10.0f} {:10.3f}'.format(float(record),
                                                        float(count), float(valid_fraction)))


def parse_arguments():
    parser = ap.ArgumentParser(description="Counts number of valid records in input_data_file.")

    parser.add_argument('missing_value', type=str,  help='Value to print.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='unused')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_count_valid_records_num(args.missing_value,
                                args.input_data_file, args.output_data_file, args.log_file)
