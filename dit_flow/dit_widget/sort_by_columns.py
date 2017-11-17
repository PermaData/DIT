""" Does multi column sort of CSV file. """

import argparse as ap
import ast
import csv

from dit_flow.dit_widget.common.logger_message import logger_message, DEFAULT_LOG_LEVEL
from dit_flow.dit_widget.common.cast_value import cast_to_datetime, \
    cast_to_integer, cast_to_real, cast_data_value, gtnp_date_time_format

date_time_index = None


def create_typed_row(row, column_list, logger):
    """
    Make sure rows to be sorted by are in sortable form.
    :param row: CSV row
    :param column_list: list of sort by column tuples (index, type)
    :return: a row of typed values
    """
    global date_time_index
    row_list = list(row)
    for index, type in column_list:
        if type == 'dt':
            date_time_index = index
            row_list[index] = cast_to_datetime(row_list[index], logger)
        elif type == 'integer':
            row_list[index] = cast_to_integer(row_list[index])
        elif type == 'real':
            row_list[index] = cast_to_real(row_list[index])
    return tuple(row_list)


def sort_by_columns(column_list, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    """
    Takes a list of columns to sort by in ascending order.
    :param input_data_file: CSV file to sort
    :param output_data_file: sorted CSV file
    :param column_list: list of tuples (index, type) describing sort columns
    """
    logger = logger_message(__name__, log_file, log_level)
    logger.info('Sorting input file by columns:')
    if isinstance(column_list, str):
        column_list = tuple_list(column_list)
    shifted_list = []
    for index, ind_type in column_list:
        index = index - 1
        new_tuple = (index, ind_type)
        logger.info('\t' + str(new_tuple))
        shifted_list.append(new_tuple)
    sorted_writer = csv.writer(open(output_data_file, 'w'), quotechar="'",
                               quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    header_row = None
    sorted_data = []
    with open(input_data_file, 'r') as csvfile:
        unsorted_reader = csv.reader(csvfile, delimiter=',', quotechar="'")
        csv_data = []
        ind = 0
        for row in unsorted_reader:
            row = [cast_data_value(col_val.strip()) for col_val in row]
            if ind > 0:
                typed_row = create_typed_row(row, shifted_list, logger)
                csv_data.append(typed_row)
            else:
                header_row = row
            ind += 1
        sorted_data = csv_data
        for index, type in reversed(shifted_list):
            sorted_data = sorted(sorted_data, key=lambda sort_by: sort_by[index])

    sorted_writer.writerow(header_row)
    for sorted_row in sorted_data:
        if date_time_index is not None:
            row_list = list(sorted_row)
            row_list[date_time_index] = row_list[date_time_index].strftime(gtnp_date_time_format)
            sorted_row = tuple(row_list)
        sorted_writer.writerow(sorted_row)


def tuple_list(tuple_string):
    try:
        data = ast.literal_eval(tuple_string)
    except:
        raise ap.ArgumentTypeError("Tuple list must be in form: \
                                   '[(<index>, <type>), (<index>, <type>)]'.")
    return data


def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser(description='Sorts 2D data in order of columns in the column list.')
    parser.add_argument('column_list', type=tuple_list, help='Ordered list of one based columns to sort by.\n'
                        'Format of list: "[(<col num>, \'<type>\'), (<col num>, \'<type>\')]"\n'
                        '<type> is the type of values of a column and can be:\n'
                        '\t\'real\'\n'
                        '\t\'int\'\n'
                        '\t\'dt\'\n'
                        '\t\'string\'\n')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    sort_by_columns(args.column_list, input_data_file=args.input_data_file,
                    output_data_file=args.output_data_file, log_file=args.log_file)
