import argparse as ap
import csv

from dit_flow.dit_widget.common.round_value import _ceil, _floor, _trunc, _round
from dit_flow.dit_widget.common.setup_logger import setup_logger


def rounding(mode, precision=0, input_data_file=None, output_data_file=None, log_file=None):
    """Round values to the nearest integer.

    modes:
        up/ceil/ceiling: round to the next integer towards +inf.
        down/floor: round to the next integer towards -inf.
        trunc/truncate: truncate decimal part, rounding towards 0.
        nearest/round: round to the nearest integer. If precision is
            given, instead round to that many digits beyond the decimal
            point.
    """
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
        data = csv.reader(_in, quoting=csv.QUOTE_NONNUMERIC)
        output = csv.writer(_out)

        input_map = {'up': _ceil, 'ceil': _ceil, 'ceiling': _ceil,
                     'down': _floor, 'floor': _floor,
                     'trunc': _trunc, 'truncate': _trunc,
                     'nearest': _round, 'round': _round,
                     }
        conv = input_map[mode.lower()]

        for line in data:
            out = []
            for item in line:
                out.append(conv(item, precision))
            output.writerow(out)


def parse_arguments():
    """ Parse the command line arguments and return them. """
    parser = ap.ArgumentParser(description="Round values to the nearest integer.")

    parser.add_argument('mode', help='Type of rounding to be done.')
    parser.add_argument('-p', '--precision', help='Precision of ending values.')

    parser.add_argument('-i', '--input_data_file', help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    rounding(args.mode, args.precision,
             args.input_data_file, args.output_data_file, args.log_file)
