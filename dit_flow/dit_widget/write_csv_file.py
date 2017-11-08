import argparse as ap

from decimal import Decimal
from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL, DEFAULT_LOG_LEVEL
from pathlib import Path


def write_csv_file(output_file, output_data, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    logger = setup_logger(__name__, log_file=log_file, log_level=log_level)
    logger.info('Writing data to file: {}'.format(output_file))
    output_path = Path(output_file)
    with output_path.open('w', newline='\n') as _to:
        for line in output_data:
            for cnt, elem in enumerate(line):
                if isinstance(elem, Decimal):
                    _to.write(str(elem))
                else:
                    _to.write("'{}'".format(elem))
                if cnt < len(line) - 1:
                    _to.write(',')
                if cnt == len(line) - 1:
                    _to.write('\n')
    output_path.touch(mode=0o666, exist_ok=True)


def parse_arguments():
    parser = ap.ArgumentParser(description="Writes CSV data matrix to a file.")

    parser.add_argument('file_name', help='Output data file name.')
    parser.add_argument('input_data', help='Data to write.')

    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    write_csv_file(args.file_name, args.input_data, args.log_file)
