#!/usr/bin/python
"""calculate VWC for 3 layers given 3 depths and three depth average VWC"""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def calc_vwc_layer(missing_value, print_flag, input_data_file=None, output_data_file=None, log_file=None):
# calculate VWC for 3 layers given 3 depths and three depth average VWC
# d1 is depth of bottom layer 1 (cm)
# d2 is depth of bottom layer 2 (cm)
# d3 is depth of bottom layer 3 (cm)
# VWC is volumetric water content from surface to d1: ratio water volume to total soil volume (m3/m3)
# V_0_d1 is VWC from surface to d1
# V_0_d2 is VWC from surface to d2
# V_0_d3 is VWC from surface to d3
# V1 is VWC for layer 1 from surface to d1
# V2 is VWC for layer 2 from d1 to d2
# V3 is VWC for layer 3 from d2 to d3

    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('calculate VWC for 3 layers given 3 depths and three depth average VWC')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            if (print_flag):
                logger.info('\t{:>15} {:>15} {:>15} {:>15} {:>15} {:>15} {:>15}'.format('d3','V_0_d1','V_0_d2','V_0_d3','VWC1','VWC2','VWC3'))
            for line in reader:
                new_line = []
                d1 = float('12')
                d2 = float('20')
                d3 = float(line[0])
                V_0_d1 = float(line[1])
                V_0_d2 = float(line[2])
                V_0_d3 = float(line[3])

# layer 1
                V1 = V_0_d1

# Layer 2
                calc_layer= True
                if (V_0_d1 == float(missing_value)):
                    calc_layer= False
                if (V_0_d2 == float(missing_value)):
                    calc_layer= False
                if (calc_layer):
                    ftop=d1/d2
                    fbot=(d2-d1)/d2
                    V2=(V_0_d2-ftop*V_0_d1)/fbot
                else:
                    V2=float(missing_value)

# Layer 3
                calc_layer= True
                if (V_0_d2 == float(missing_value)):
                    calc_layer= False
                if (V_0_d3 == float(missing_value)):
                    calc_layer= False
                if (d3 == float(missing_value)):
                    calc_layer= False
                if (calc_layer):
                    ftop=d2/d3
                    fbot=(d3-d2)/d3
                    V3=(V_0_d3-ftop*V_0_d2)/fbot
                else:
                    V3=float(missing_value)

                if (print_flag):
                    logger.info('\t{:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f}'.format(d3, V_0_d1, V_0_d2, V_0_d3, V1, V2, V3))
                new_line.append(V1)
                new_line.append(V2)
                new_line.append(V3)
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

    calc_vwc_layer(args.missing_value, args.input_data_file, args.output_data_file, args.log_file)
