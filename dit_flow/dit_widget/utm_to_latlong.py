#! /usr/bin/python

import csv

import utm
import argparse as ap

from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


def utm_to_latlong(input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    """Converts UTM coordinates into latitude/longitude.
    assumes rows are easting, northing, zone number, either 'N' for northern
    hemisphere or 'S' for southern hemisphere
    """
    logger = setup_logger(__name__, log_file, log_level)

    # Check required input and output data file names were given.
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'

    _in = open(input_data_file, 'r')
    try:
        _out = open(output_data_file, 'w')
        try:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for row_ind, row in enumerate(data):
                east = float(row[0])
                north = float(row[1])
                zone = int(row[2])

                latlong = utm.to_latlon(east, north, zone, northern=('N' == row[3]))
                logger.info('Changed row {} from: {}  to: {}'.format(row_ind,
                                                                     (row[0], row[1]), latlong))

                output.writerow(latlong)
        finally:
            _out.close()
    finally:
        _in.close()


def parse_arguments():
    parser = ap.ArgumentParser(description='Converts UTM coordinates into latitude/longitude.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    utm_to_latlong(args.input_data_file, args.output_data_file, args.log_file)
