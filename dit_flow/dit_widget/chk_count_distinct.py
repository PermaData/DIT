#!/usr/bin/python
"""Counts number of distinct values in a column."""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def chk_count_distinct(print_flag, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Counts number of distinct values in input_data_file.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    record = 0
    with open(input_data_file, newline='') as _in:
        logger.info('Count distinct values')
        reader = csv.reader(_in)
        temp_distinct_values = set()
        original_values = []
        distinct_values = []

# identify distinct values, transfer input values to array
        for line in reader:
            for item in line:
                record = record + 1
                temp_distinct_values.add(item)
                original_values.append(item)
        logger.info('\tTotal number ={}'.format(record))

# set array randomly changes order with each execution, so transfer to array and sort
        for value in temp_distinct_values:
            distinct_values.append(value)
        distinct_values.sort()

# count number records for each value
        if print_flag:
            logger.info('{:>5} {:>40} {:>10} {:>10}'.format('Num',
                                                            'Distinct Value', 'number', 'Percent'))
            count = 0
            for value in distinct_values:
                count = count+1
                number = original_values.count(value)
                num_fraction = float(number)/float(record)*100
                logger.info('{:5.0f} {:>40} {:10.0f} {:10.3f}'.format(count,
                                                                  value, number, num_fraction))


def parse_arguments():
    parser = ap.ArgumentParser(description="Counts number of distinct values in input_data_file.")

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='unused')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_count_distinct(args.input_data_file, args.output_data_file, args.log_file)
