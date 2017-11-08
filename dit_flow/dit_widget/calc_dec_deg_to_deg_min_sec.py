#!/usr/bin/python
"""Convert decimal degrees to degrees minutes seconds"""
import argparse as ap
import csv
import math
from array import array

from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


def calc_dec_deg_to_deg_min_sec(missing_value, input_data_file=None,
                                output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    #   Convert degrees minutes seconds to decimal degrees
    logger = setup_logger(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Convert degrees minutes seconds to decimal degrees')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                new_line = array('f')
                if (float(line[0]) != float(missing_value)):
                    decimal_degree = math.fabs(float(line[0]))
                    sign = float(line[0])/math.fabs(float(line[0]))
                    degree = math.trunc(decimal_degree)
                    minute = (decimal_degree-degree)*60.
                    second = (minute-math.trunc(minute))*60.
                    minute = math.trunc(minute)
                    degree = sign*degree
                else:
                    degree = float(missing_value)
                    minute = float(missing_value)
                    second = float(missing_value)
                new_line.append(degree)
                new_line.append(minute)
                new_line.append(second)
#               output.writerow(new_line)
#               output.writerow(['{:.0f},{:.0f},{:.4f}'.format(new_line)])
                output.writerow(['{:.0f}'.format(x) for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description='Convert decimal degrees to degrees minutes seconds.')

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_dec_deg_to_deg_min_sec(args.missing_value, args.input_data_file,
                                args.output_data_file, args.log_file)
