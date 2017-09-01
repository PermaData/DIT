import argparse as ap

# setup_logger is offered as a convenience method for creating Python standard
# logging file and stream that will duplicate output to the screen.
from dit_flow.dit_widget.common.setup_logger import setup_logger

# The three required keyword arguments (input_data_file, output_data_file, and
# log_file) will be called by keyword and needn't be used by the widget.
def widget_template(method_arg_1, method_arg_2, input_data_file=None, output_data_file=None, log_file=None):
    if log_file:
        logger = setup_logger(__name__, log_file)
        logger.info('I am a widget. Here are my arguments:')
        logger.info('\tinput_data_file = {}'.format(input_data_file))
        logger.info('\toutput_data_file = {}'.format(output_data_file))
        logger.info('\tlog_file = {}'.format(log_file))
        logger.info('\tmethod_arg_1 = {}'.format(method_arg_1))
        logger.info('\tmethod_arg_2 = {}'.format(method_arg_2))
    else:
        print('I am a widget. Here are my arguments:')
        print('\tinput_data_file = {}'.format(input_data_file))
        print('\toutput_data_file = {}'.format(output_data_file))
        print('\tlog_file = {}'.format(log_file))
        print('\tmethod_arg_1 = {}'.format(method_arg_1))
        print('\tmethod_arg_2 = {}'.format(method_arg_2))


def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser(description="Does a cool data manipulation.")

    # These arguments represent additional arguments needed by this widget to
    # do its manipulation. There may not be any or there may be many.
    parser.add_argument('method_arg_1', help='Argument needed by manipulation method.')
    parser.add_argument('method_arg_2', help='Argument needed by manipulation method.')

    # These arguments represent the interface between DIT and this manipulation.
    # They are therefore mandatory arguments for a widget method.
    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    widget_template(args.method_arg_1, args.method_arg_2,
                    args.input_data_file, args.output_data_file, args.log_file)
