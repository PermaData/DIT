#!/usr/bin/python
"""Makes a kml wal file with height of wall = variable"""
import argparse as ap
import csv
import simplekml

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL


def make_kml_wall(missing_value, multiplier, input_data_file=None, output_data_file=None, log_file=None):
# Makes a kml wal file with height of wall = variable
    logger = logger_message(__name__, log_file)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'A kml point file.'
    with open(input_data_file, newline='') as _in:
        logger.info('Make kml wall file: {}'.format(output_data_file))
        reader = csv.reader(_in)

# transfer input values to local array
        original_values = []
        points = 0
        for i, line in enumerate(reader):
                points = points + 1
                original_values.append([])
                for j, item in enumerate(line):
                    original_values[i].append(item)

# line[0] = line name or id (treated as string)
# line[1] = longitude decimal degree
# line[2] = latitude decimal degree
# line[3] = variabe to serve as height of wall (z-variable)

# count distinct lines
    temp_distinct_values = set()
    distinct_values = []
    for i, line in enumerate(original_values):
        temp_distinct_values.add(line[0])
    for value in temp_distinct_values:
        distinct_values.append(value)
    distinct_values.sort()

# extract coordinates
    kml = simplekml.Kml()
    zero = 0.0
    for value in distinct_values:
        coordinates = []
        count = 0
        for i, line in enumerate(original_values):
            if(value == line[0]):
                add_pt = True
                if(float(line[1]) == float(missing_value)):
                    add_pt = False
                if(float(line[2]) == float(missing_value)):
                    add_pt = False
                if(add_pt):
                    coordinates.append([])
                    coordinates[count].append(line[1])
                    coordinates[count].append(line[2])
                    if(float(line[3]) == float(missing_value)):
                        coordinates[count].append(zero)
                    else:
                        height = float(line[3]) * float(multiplier)
                        coordinates[count].append(height)
                    count = count + 1
        ls = kml.newlinestring(name='{}'.format(value))
        ls.coords = coordinates
        ls.extrude = 1
        ls.altitudemode = simplekml.AltitudeMode.relativetoground
        ls.style.linestyle.width = 5
        ls.style.linestyle.color = simplekml.Color.blue
    kml.save(output_data_file)

def parse_arguments():
    parser = ap.ArgumentParser(description="Makes a kml point file.")
    parser.add_argument('missing_value', type=float, help='Missing data value in file.')
    parser.add_argument('multiplier', type=float, help='multiplier for hieght of wall')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='output kml file.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    make_kml_wall(args.constant, args.multiplier, args.input_data_file, args.output_data_file, args.log_file)
