#!/usr/bin/python
"""calculate VWC given TWTT and ALT"""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def calc_vwc_gpr(missing_value, print_flag, input_data_file=None, output_data_file=None, log_file=None):
# calculate VWC given TWTT and ALT
# TWTT is two way travel time from Ground penetrating radar (ns)
# VWC is volumetric water content: ratio water volume to total soil volume (m3/m3)
# ALT is active layer thickness: maximum thaw depth at end of summer (cm)
# velocity = wave velocity (cm/ns)

    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Calculate VWC given TWTT and ALT')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            if (print_flag):
                logger.info('\t{:>15} {:>15} {:>15} {:>15} {:>15}'.format('twtt (ns)','alt (cm)','velocity (cm/ns)', 'dielectric (-)', 'vwc (-)'))
            for line in reader:
                new_line = []
                twtt = float(line[0])
                alt = float(line[1])
                if (twtt != float(missing_value)) and \
                   (alt != float(missing_value)):
                    velocity = float(line[1]) * 2. /float(line[0])
                    dielectric = (30./velocity)**2.
                    vwc = -2.5 + 2.508 * dielectric - 3.634e-2 * dielectric * dielectric
                    vwc = vwc + 2.394e-4 * dielectric*dielectric*dielectric
                    vwc = vwc /100.
                    vwc = min(vwc, 1.)
                else:
                    velocity = float(missing_value)
                    dielectric = float(missing_value)
                    vwc = float(missing_value)
                if (print_flag):
                    logger.info('\t{:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f}'.format(twtt,alt,velocity, dielectric, vwc))
                new_line.append(velocity)
                new_line.append(dielectric)
                new_line.append(vwc)
                output.writerow(new_line)


def parse_arguments():
    parser = ap.ArgumentParser(description='Add two columns (out = column_a +column_b).')

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')
    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    calc_vwc_gpr(args.missing_value, args.input_data_file, args.output_data_file, args.log_file)
