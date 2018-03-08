#!/usr/bin/python
"""Interpolates per site values of one column based on relative spacing in another column"""
import argparse as ap
import csv

from dit_flow.dit_widget.common.cast_value import cast_float_to_decimal
from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL

def math_interp_relative(missing_value, print_flag, input_data_file=None, output_data_file=None, log_file=None):
# Interpolates per site values of one column based on relative spacing in another column
# assumes input array has three columns:
# col1: site ID treated as string 
# col2: column that determines relative spacing
# col3: interpolated column
# assumes input array already sorted by col1 and col2
# assumes first and last values for each site are valid
# assumes all col1 and col2 values are valid

    logger = logger_message(__name__, log_file)
    logger.info('Interpolate by Site and relative value')
    assert input_data_file is not None, 'An input CSV file with columns of values to be added to is required.'
    assert output_data_file is not None, 'An output CSV file to write new values to is required.'

# read input data to local array
    with open(input_data_file, newline='') as _in:
        reader = csv.reader(_in)
        input_data = []
        num_in_record = 0
        for i, line in enumerate(reader):
            num_in_record = num_in_record + 1
            input_data.append(line)
        logger.info('\tNumber in records: {}'.format(num_in_record))

# identify unique sites
    temp_distinct_sites = set()
    distinct_sites = []
    for i, line_in in enumerate(input_data):
        temp_distinct_sites.add(line_in[0])
    num_sites = 0
    for value in temp_distinct_sites:
        num_sites = num_sites+1
        distinct_sites.append(value)
    distinct_sites.sort()
    logger.info('\tnumber sites: {} '.format(num_sites))

# extract data to interpolate and perform interpolation for each site
    for i in range(num_sites):
        num_pts = 0
        num_valid_pts = 0
        indeces = []
        xval = []
        yval = []
        valid = []
        for j, line_in in enumerate(input_data):
            if (line_in[0] == distinct_sites[i]):
               num_pts = num_pts+1
               indeces.append(j)
               xval.append(float(line_in[1]))
               yval.append(float(line_in[2]))
               if (float(line_in[2]) == float(missing_value)):
                   valid.append('False')
               else:
                   num_valid_pts = num_valid_pts+1
                   valid.append('True')

# Check to see if you can interpolate
        interpolate_flag = True
        if (num_pts <= 2):
            interpolate_flag = False
            logger.info('\tNot enough points to interpolate {}'.format(distinct_sites[i]))
            logger.info('\t\tNumber points: {}'.format(num_pts))
        if (num_valid_pts <= 1):
            interpolate_flag = False
            logger.info('\tNot enough valid points to interpolate {}'.format(distinct_sites[i]))
            logger.info('\t\tNumber valid points: {}'.format(num_valid_pts))
        if (yval[0] == float(missing_value)):
            interpolate_flag = False
            logger.info('\tFirst point must be valid to interpolate {}'.format(distinct_sites[i]))
            logger.info('\t\tFirst point: {}'.format(yval[0]))
        if (yval[num_pts-1] == float(missing_value)):
            interpolate_flag = False
            logger.info('\tLast point must be valid to interpolate {}'.format(distinct_sites[i]))
            logger.info('\t\tLast point: {}'.format(yval[num_pts-1]))
        if (interpolate_flag):
            logger.info('\tInterpolate: {}'.format(distinct_sites[i]))

# find interpolation points
        if (interpolate_flag):
            num_segments = 0
            segment_number = []
            x1 = []
            y1 = []
            x2 = []
            y2 = []
            x1.append(xval[0])
            y1.append(yval[0])
            for j in range(num_pts):
                segment_number.append(num_segments)
                if (valid[j] == 'True' and j > 1):
                    num_segments = num_segments + 1
                    x2.append(xval[j])
                    y2.append(yval[j])
                    x1.append(xval[j])
                    y1.append(yval[j])
            x1.append(xval[num_pts-1])
            y1.append(yval[num_pts-1])
            if (print_flag):
                logger.info('\tnum_pts: {} num_valid_pts: {}'.format(num_pts, num_valid_pts))
                logger.info('\tnumber interpolate segments: {} '.format(num_segments))
                logger.info('\t\t {:>10} {:>15} {:>15} {:>15} {:>15}'.format('seg','x1','x2','y1','y2'))
                for k in range(num_segments):
                    logger.info('\t\t {:>10.0f} {:>15.7f} {:>15.7f} {:>15.7f} {:>15.7f}'.format(k,x1[k],x2[k],y1[k],y2[k]))

# actual interpolation
            interp_yval = []
            for j in range(num_pts):
                k = segment_number[j]
                if (valid[j] == 'False'):
#                    logger.info('\t\tk: {} x1: {} x2: {} y1: {} y2: {}'.format(k,x1[k],x2[k],y1[k],y2[k]))
                    if (x2[k] == x1[k]):
                        interp_yval.append(missing_value)
                    else:
                        slope = (y2[k]-y1[k])/(x2[k]-x1[k])
                        temp_y = y1[k] + (xval[j]-x1[k])*slope
                        interp_yval.append(temp_y)
                else:
                    interp_yval.append(yval[j])

            if (print_flag):
                logger.info('\t\t {:>10} {:>15} {:>15} {:>15}'.format('record','x','y_old','y_int'))
                for j in range(num_pts):
                    logger.info('\t\t {:>10.0f} {:>15.7f} {:>15.7f} {:>15.7f}'.format(indeces[j],xval[j], yval[j],interp_yval[j]))

# transfer interpolated values to output array
            k = 0
            output_data = []
            for j, line_in in enumerate(input_data):
                if (line_in[0] == distinct_sites[i]):
                    line_in[2] = interp_yval[k]
                    k=k+1
                output_data.append(line_in)

# write output data
    with open(output_data_file, 'w', newline='') as _out:
        output = csv.writer(_out)
        for line in output_data:
            output.writerow(line)

def is_number(s):  # checks if the item in list is a number
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_arguments():
    parser = ap.ArgumentParser(description="Interpolates per site values of one column based on relative spacing in another column")

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')
    parser.add_argument('print_flag', type=bool, help='Printing option value.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    math_interp_relative(args.missing_value, args.input_data_file, args.output_data_file, args.log_file)
