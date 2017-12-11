#!/usr/bin/python
"""Makes a kml point file."""
import argparse as ap
import csv
import simplekml

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def make_kml_point(input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Makes a kml point file.
    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'A kml point file.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
        logger.info('Make kml point file: {}'.format(output_data_file))
        output = csv.writer(_out)
        reader = csv.reader(_in)
        original_values = []

# transfer input values to local array
        points = 0
        for i, line in enumerate(reader):
                points = points + 1
                original_values.append([])
                for j, item in enumerate(line):
                    original_values[i].append(item)
        logger.info('\tNumber points: {}'.format(points))

# make kml point file
    kml = simplekml.Kml()
    for i, line in enumerate(original_values):
        pnt = kml.newpoint(name=line[0], coords=[(line[1], line[2])])
    kml.save(output_data_file)


def parse_arguments():
    parser = ap.ArgumentParser(description="Makes a kml point file.")

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='output kml file.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    make_kml_point(args.input_data_file, args.output_data_file, args.log_file)
