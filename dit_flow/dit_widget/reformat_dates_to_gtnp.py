""" Reformats a file of one column of date/times into GTN-P specific date/time format. """

import argparse as ap
import csv
import datetime as dt

from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL

gtnp_date_time_format = '%Y-%m-%d %H:%M'


def reformat_dates_to_gtnp(date_time_format, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    """
    Reformat the date/times.
    :param column_file: file containing date/time column
    :param out_file: CSV filename for reformatted date/times
    :param in_format: python strptime format string of date/times in column_file
    """
    logger = setup_logger(__name__, log_file, log_level)
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
        data = csv.reader(_in)
        output = csv.writer(_out)
        for line in data:
            for i, item in enumerate(line):
                try:
                    date_time = dt.datetime.strptime(item.strip(), date_time_format)
                    quoted_dt = "'{0}'".format(date_time.strftime(gtnp_date_time_format))
                    line[i] = quoted_dt
                except ValueError as error:
                    logger.error(error)
            output.writerow(line)
    # date_time_writer = csv.writer(open(out_file, 'wb'), lineterminator='\n')
    # with open(column_file, 'rb') as csvfile:
    #     date_time_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in date_time_reader:
    #         try:
    #             date_time = dt.datetime.strptime(row[0].strip(), in_format)
    #             quoted_dt = "{0}".format(date_time.strftime(gtnp_date_time_format))
    #             date_time_writer.writerow([quoted_dt])
    #         except ValueError as error:
    #             print(error)
    #             date_time_writer.writerow(row)


def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser(description="Does a cool data manipulation.")

    parser.add_argument('date_time_format', help='Python strptime format string of date/times in column_file.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    reformat_dates_to_gtnp(args.method_arg_1, args.method_arg_2,
                           args.input_data_file, args.output_data_file,
                           args.log_file)
