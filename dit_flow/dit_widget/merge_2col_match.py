#!/usr/bin/python
"""Merges two files by matching values in two columns"""
import argparse as ap
import csv
from array import array

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL

def merge_2col_match(in_col1, in_col2, merge_col1, merge_col2, map_file, merge_file, 
                     input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
# Merges two files by matching values in two columns 

    logger = logger_message(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    logger.info('Merge Files')

# save some messages to log file
    logger.info('\tMerge file: {}'.format(merge_file))
    logger.info('\tMap file: {}'.format(map_file))


# read in all variable mapping information for inserting merge_file into input_data_file
    col_number = []
    in_name = []
    operation = []
    out_name = []
    in_index = []
    out_index = []
    units = []
    description = []
    num_map_record = 0
    with open(map_file, newline='') as _in:
#        logger.info('\tRead merge Variable Mapping File')
        reader = csv.reader(_in)
        firstline = True
        for line in reader:
#            logger.info('{}'.format(line))
            if (firstline):
                # skips first line
                firstline = False
                continue
            num_map_record = num_map_record +1
            col_number.append(line[0])
            in_name.append(line[1])
            operation.append(line[2])
            out_name.append(line[3])
            in_index.append(line[4])
            out_index.append(line[5])
            units.append(line[6])
            description.append(line[7])
#        logger.info('\tNumber map records: {} '.format(num_map_record))
 
# Figure out which columns to copy
    num_copies = 0
    copy_from=[]
    copy_to=[]
    for i in range(num_map_record):
        if (operation[i] == 'copy'):
            copy_from.append(int(in_index[i])-1)
            copy_to.append(int(out_index[i])-1)
#            logger.info('\toperation: {} {} '.format(copy_from[num_copies],copy_to[num_copies]))
            num_copies = num_copies + 1
    logger.info('\tnum_copies: {} '.format(num_copies))

# adjust column numbers to zero start
    in_col1 = in_col1 - 1
    in_col2 = in_col2 - 1
    merge_col1 = merge_col1 - 1
    merge_col2 = merge_col2 - 1

# read input data to local array
    with open(input_data_file, newline='') as _in:
        reader = csv.reader(_in)
        input_data = []
        num_in_record = 0
        for i, line in enumerate(reader):
            num_in_record = num_in_record + 1
            input_data.append(line)
#        logger.info('\tNumber in records: {}'.format(num_in_record))

# read merge data to local array
    unmatched = []
    with open(merge_file, newline='') as _in:
        reader = csv.reader(_in)
        merge_data = []
        num_merge_record = 0
        firstline = True
        for i, line in enumerate(reader):
            if (firstline):
                firstline = False
                continue
            num_merge_record = num_merge_record + 1
            unmatched.append('true')
            merge_data.append(line)
#        logger.info('\tNumber merge file records: {}'.format(num_merge_record))

# merge the two files
    output_data = []
    num_records_merged = 0
    for i, line_in in enumerate(input_data):
        for j, line_merge in enumerate(merge_data):
            if (line_merge[merge_col1] == line_in[in_col1]):
                if (line_merge[merge_col2] == line_in[in_col2]):
                    num_records_merged = num_records_merged + 1
                    unmatched[j] = 'false'
                    for k in range(num_copies):
                        line_in[copy_to[k]]=line_merge[copy_from[k]]
#                        logger.info('\tcopy: {} {} '.format(line_merge[copy_from[k]],line_in[copy_to[k]]))
        output_data.append(line_in)
    logger.info('\tRecords merged input file: {}'.format(num_records_merged))

# write output data
    with open(output_data_file, 'w', newline='') as _out:
        output = csv.writer(_out)
        for line in output_data:
            output.writerow(line)

# count unmatched records in merge file
    num_unmatched = 0
    num_matched = 0
    for i, line_merge in enumerate(merge_data):
        if (unmatched[i]=='true'):
            num_unmatched = num_unmatched + 1
        else:
            num_matched = num_matched + 1
 
# print unmatched records
    if (num_unmatched != 0):
        logger.info('\tUnmatched records in merge file: {}'.format(num_unmatched))
        logger.info('\t{:>5} {:>30} {:>30}'.format('Rec','col1','col2'))
        for i, line_merge in enumerate(merge_data):
            if (unmatched[i]=='true'):
                logger.info('\t{:>5} {:>30} {:>30}'.format(i + 1,line_merge[merge_col1],line_merge[merge_col2]))

def parse_arguments():
    parser = ap.ArgumentParser(description="merges two files by marching values in two columns")

    parser.add_argument('in_col1', help='First column input file to match')
    parser.add_argument('in_col2', help='Second column input file to match')
    parser.add_argument('merge_col1', help='First column merge file to match')
    parser.add_argument('merge_col2', help='Second column merge file to match')
    parser.add_argument('map_file', help='variable mapping file merge_file to input_data_file.')
    parser.add_argument('merge_file', help='data to merge with input_data_file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='unused')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    merge_2col_match(args.in_col1, args.in_col2, args.merge_col1, args.merge_col2,
                   args.map_file, args.merge_file,
                   args.input_data_file, args.output_data_file, args.log_file)
