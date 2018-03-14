#!/usr/bin/python
"""Replaces empty array location (empty string) with text string"""
import argparse as ap
import csv
import re

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def replace_txt_empty(replace, print_flag, input_data_file=None,
                      output_data_file=None, log_file=None):
# Replaces empty array location (empty string) with text string
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    count = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Replacing empty string with {}'.format(replace))
            if print_flag:
                logger.info('{:>10} {:>20}'.format('Record',  'New Value'))
            output = csv.writer(_out)
            reader = csv.reader(_in)
            test=''
            for line in reader:
                modified_text = line
                for i, item in enumerate(line):
                    record = record + 1
                    logger.info('{}'.format(item))
                    if (item == test):
                        if print_flag:
                            logger.info('{:10.0f} {:>20}'.format(float(record),replace))
                        count = count + 1
                        modified_text[i] = replace
                    else:
                        modified_text[i] = item
                output.writerow(modified_text)
            logger.info('\n\t Total number ={}'.format(count))


def parse_arguments():

    parser = ap.ArgumentParser(description="Replaces empty array location (empty string) with text string")

    parser.add_argument('replace', type=str, help='Replacement text string.')
    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    replace_txt_empty(args.replace, args.print_flag,
                      args.input_data_file, args.output_data_file, args.log_file)
