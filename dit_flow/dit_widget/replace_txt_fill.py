#!/usr/bin/python
"""Fills column with text string."""
import argparse as ap
import csv

from dit_flow.dit_widget.common.logger_message import logger_message


def replace_txt_fill(fill, input_data_file=None, output_data_file=None, log_file=None):
    # Fills input_data_file with text string and writes result to output_data_file.
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    record = 0
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Filling with {}'.format(fill))
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                modified_text = line
                for i, item in enumerate(line):
                    record = record + 1
                    modified_text[i] = fill
                output.writerow(modified_text)
            logger.info('\n\t Total number ={}'.format(record))


def parse_arguments():
    parser = ap.ArgumentParser(description="Fills input_data_file with text string"
                               "and writes the result to "
                               "output_data_file.")

    parser.add_argument('fill', type=str, help='Text string to fill.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    replace_txt_fill(args.fill,
                     args.input_data_file, args.output_data_file, args.log_file)
