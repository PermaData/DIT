#!/usr/bin/python
"""Adds a constant to all numeric values in a column file."""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.setup_logger import setup_logger
from dit_flow.dit_widget.common.to_decimal import str_to_dec, prec_from_str, float_to_dec
from decimal import localcontext


def math_add_constant(constant, missing_value, input_data_file=None, output_data_file=None, log_file=None):
    # Adds constant to all values in input_data_file and writes the result to
    # output_data_file.
    logger = setup_logger(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
        logger.info('Adding {} to the column'.format(constant))
        output = csv.writer(_out)
        reader = csv.reader(_in)
        for line in reader:
            with localcontext() as localctx:
                new_line = array('f')
                for item in line:
                    localctx.prec = prec_from_str(item, logger)
                    dec_item = str_to_dec(item, logger)
                    print('dec_item = ', dec_item)

                    if isinstance(missing_value, float):
                        print('making dec from float ', missing_value, ' with precision: ', localctx.prec)
                        dec_missing = float_to_dec(missing_value, localctx.prec, logger)
                    else:
                        print('making dec from missing ', missing_value)
                        dec_missing = str_to_dec(missing_value, logger)

                    if isinstance(constant, float):
                        print('making dec from constant float ', constant, ' with precision: ', localctx.prec)
                        dec_constant = float_to_dec(constant, localctx.prec, logger)
                    else:
                        print('making dec from constant ', constant)
                        dec_constant = str_to_dec(constant, logger)

                    print("item: ", dec_item, "  missing: ", dec_missing, "  constant: ", dec_constant)
                    if dec_item != dec_missing:
                        value = dec_item + dec_constant
                    else:
                        value = dec_missing
                    new_line.append(value)
                output.writerow([x for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description="Adds constant to all values in "
                               "input_data_file and writes the result to "
                               "output_data_file.")

    parser.add_argument('constant', type=float, help='Constant to be added to the column values.')
    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    math_add_constant(args.constant, args.missing_value,
                      args.input_data_file, args.output_data_file, args.log_file)
