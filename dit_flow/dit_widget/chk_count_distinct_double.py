#!/usr/bin/python
"""Counts number of distinct values in a col A then corresponing distinct values in col B."""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message


def chk_count_distinct_double(input_data_file=None, output_data_file=None, log_file=None):
    # Counts number of distinct values in a col A
    # then corresponing distinct values in col B in input_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    with open(input_data_file, newline='') as _in:
        logger.info('Count distinct values')
        reader = csv.reader(_in)
        temp_col_a_distinct = set()
        col_a_distinct = []
        column_a_values = []
        column_b_values = []
        original_values = []

# transfer input values to local array
        record = 0
        for i, line in enumerate(reader):
            record = record + 1
            original_values.append([])
            for item in line:
                original_values[i].append(item)
        logger.info('\tTotal number ={}'.format(record))

# identify column A distinct values, transfer original values to col A/B arrays
        for i, line in enumerate(original_values):
            temp_col_a_distinct.add(original_values[i][0])
            column_a_values.append(original_values[i][0])
            column_b_values.append(original_values[i][1])

# transfer col A distinct values from temporary to permanent array and sort
        for value in temp_col_a_distinct:
            col_a_distinct.append(value)
        col_a_distinct.sort()

# count number records in column B for each distinct col A value
        logger.info('{:>5} {:>40} {:>40} {:>10} {:>10}'.format('Num', 'Col A Value',
                                                               'Col B Value', 'number', 'Percent'))
        count = 0
        for value in col_a_distinct:

# subset column B array and identify distinct col B values
            col_b_subset = []
            temp_col_b_distinct = set()
            col_b_distinct = []
            for i, subset in enumerate(column_a_values):
                if subset == value:
                    col_b_subset.append(column_b_values[i])
                    temp_col_b_distinct.add(column_b_values[i])

# transfer col b distinct values from temporary to permanent array and sort
            for subset in temp_col_b_distinct:
                col_b_distinct.append(subset)
            col_b_distinct.sort()

# write results to log file
            for subset in col_b_distinct:
                count = count+1
                number = col_b_subset.count(subset)
                num_fraction = float(number)/float(record)*100
                logger.info('{:5.0f} {:>40} {:>40} {:10.0f} {:10.3f}'.format(count, value, subset,
                                                                             number, num_fraction))


def parse_arguments():
    parser = ap.ArgumentParser(description="Counts number of distinct values in a col A then corresponing distinct values in col B in input_data_file.")

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='unused')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_count_distinct_double(args.input_data_file, args.output_data_file, args.log_file)
