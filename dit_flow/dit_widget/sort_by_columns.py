""" Does multi column sort of CSV file. """

import argparse as ap
import ast
import csv
import datetime as dt

from dit_flow.dit_widget.common.setup_logger import setup_logger

gtnp_date_time_format1 = '%Y-%m-%d %H:%M'
gtnp_date_time_format2 = '%Y-%m-%d %H:%M:%S'
gtnp_date_time_format = gtnp_date_time_format1
date_time_index = None


def cast_to_datetime(dt_str, logger=None):
    """
    Convert string to a datetime object.
    :param int_str: string to convert to a datetime object
    :return: datetime object
    """
    date_time = None
    dt_str = dt_str.strip()
    try:
        gtnp_date_time_format = gtnp_date_time_format1
        date_time = dt.datetime.strptime(dt_str, gtnp_date_time_format)
    except ValueError as error:
        try:
            gtnp_date_time_format = gtnp_date_time_format2
            date_time = dt.datetime.strptime(dt_str, gtnp_date_time_format)
        except ValueError as error:
            logger.error('"', error, '"')
            logger.error('Column cannot be converted to date/time. Sorting will be by string.')
    return date_time


def cast_to_integer(int_str):
    """
    Convert string to an integer.
    :param int_str: string to convert to an integer
    :return: integer number
    """
    try:
        return int(float(int_str))
    except ValueError:
        return int_str


def cast_to_real(real_str):
    """
    Convert string to a real.
    :param real_str: string to convert to a real
    :return: real number
    """
    try:
        return float(real_str)
    except ValueError:
        return real_str


def cast_data_value(col_str):
    """
    Cast strings to integers or reals before writing them to the file to avoid
    quoting numerics.
    :param col_str: data string value to possible cast
    :return: an integer, real, or string
    """
    try:
        return int(col_str)
    except ValueError:
        pass
    try:
        return float(col_str)
    except ValueError:
        pass
    return col_str


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


def sort_by_columns(column_list, input_data_file=None, output_data_file=None, log_file=None):
    """
    Takes a list of columns to sort by in ascending order.
    :param input_data_file: CSV file to sort
    :param output_data_file: sorted CSV file
    :param column_list: list of tuples (index, type) describing sort columns
    """
    logger = setup_logger(__name__, log_file)
    logger.info('Sorting input file by columns:')
    for column in column_list:
        logger.info('\t' + str(column))
    sorted_writer = csv.writer(open(output_data_file, 'w'), quotechar="'", quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    header_row = None
    sorted_data = []
    with open(input_data_file, 'r') as csvfile:
        unsorted_reader = csv.reader(csvfile, delimiter=',')
        csv_data = []
        ind = 0
        for row in unsorted_reader:
            row = [cast_data_value(col_val.strip()) for col_val in row]
            print('row: ', row)
            if ind > 0:
                typed_row = create_typed_row(row, column_list, logger)
                csv_data.append(typed_row)
            else:
                header_row = row
            ind += 1
        sorted_data = csv_data
        for index, type in reversed(column_list):
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
        print('argument: ', tuple_string)
        data = ast.literal_eval(tuple_string)
    except:
        raise ap.ArgumentTypeError("Tuple list must be in form: '[(<index>, <type>), (<index>, <type>)]'.")
    return data


def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser(description='Sorts 2D data in order of columns in the column list.')
    parser.add_argument('column_list', type=tuple_list, help='Ordered list of columns to sort by.\n'
                        'Format of list: "[(<col num>, \'<type>\'), (<col num>, \'<type>\')]"\n'
                        '<type> is the type of values of a column and can be:\n'
                        '\t\'real\'\n'
                        '\t\'int\'\n'
                        '\t\'dt\'\n'
                        '\t\'string\'\n')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    sort_by_columns(args.column_list, input_data_file=args.input_data_file,
                    output_data_file=args.output_data_file, log_file=args.log_file)
