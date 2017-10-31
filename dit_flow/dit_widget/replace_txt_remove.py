#!/usr/bin/python
"""Removes text string from a column."""
import argparse as ap
import csv
import re

from dit_flow.dit_widget.common.logger_message import logger_message


def replace_txt_remove(target, print_flag, input_data_file=None,
                       output_data_file=None, log_file=None):
    # Removes target text string from input_data_file and writes result to output_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    replace = ''
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Removing {}'.format(target))
            if print_flag:
                logger.info('{:>10} {:>20} {:>20}'.format('Record', 'Old Value', 'New Value'))
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                modified_text = line
                for i, item in enumerate(line):
                    record = record + 1
                    modified_text[i] = item
                    if re.search(target, item):
                        count = count+1
                        modified_text[i] = re.sub(target, replace, item)
                        if print_flag:
                            logger.info('{:10.0f} {:>20} {:>20}'.format(float(record), item,
                                        modified_text[i]))
                    else:
                        modified_text[i] = item
                output.writerow(modified_text)
            logger.info('\n\t Total number ={}'.format(count))


def parse_arguments():
    parser = ap.ArgumentParser(description=" Removes target text string from"
                               "input_data_file and writes the result to "
                               "output_data_file.")

    parser.add_argument('target', type=str, help='Text string to remove.')
    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    replace_txt_remove(args.target, args.print_flag,
                       args.input_data_file, args.output_data_file, args.log_file)
