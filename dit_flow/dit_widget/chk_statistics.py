#!/usr/bin/python
"""Calculates statistics for each input column."""
import argparse as ap
import csv
import statistics

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def chk_statistics(missing_value, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Calculates statistics for each input column in input_data_file.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    with open(input_data_file, newline='') as _in:
        logger.info('Calculate Statistics')
        reader = csv.reader(_in)
        original_values = []

# transfer input values to local array
        record = 0
        for i, line in enumerate(reader):
            record = record + 1
            original_values.append([])
            column = 0
            for j, item in enumerate(line):
                column = column+1
                original_values[i].append(item)
        logger.info('\tTotal number ={}'.format(column))

# extract valid values each column and calculate statistics
        logger.info('{:>4}{:>6}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}'
                    .format('Col', 'nrec', 'Mean', 'Stdev', 'Min', '1st_qrtl', 'Median', '3rd_qrtl', 'Max'))
        for i in range(column):
            Column_valid = []
            count = 0
            for j, line in enumerate(original_values):
                if float(line[i]) != float(missing_value):
                    count = count + 1
                    Column_valid.append(float(line[i]))
            Column_valid.sort()
            middle = int(count/2.)
            mean = statistics.mean(Column_valid)
            stdev = statistics.stdev(Column_valid)
            minimum = min(Column_valid)
            percentile_25 = statistics.median(Column_valid[:middle])
            median = statistics.median(Column_valid)
            percentile_75 = statistics.median(Column_valid[middle:])
            maximum = max(Column_valid)
            logger.info('{:>4.0f}{:>6.0f}{:>10.3f}{:>10.3f}{:>10.3f}{:>10.3f}{:>10.3f}{:>10.3f}{:>10.3f}'
                        .format(i+1, count, mean, stdev, minimum, percentile_25, median, percentile_75, maximum))


def parse_arguments():
    parser = ap.ArgumentParser(description="Counts number of distinct values in a col A \
                               then corresponing distinct values in col B in input_data_file.")

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='unused')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    chk_statistics(args.missing_value,
                   args.input_data_file, args.output_data_file, args.log_file)
