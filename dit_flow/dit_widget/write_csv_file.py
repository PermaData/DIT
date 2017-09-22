import argparse as ap

from dit_flow.dit_widget.common.setup_logger import setup_logger


def write_csv_file(output_file, output_data, log_file=None):
    logger = setup_logger(__name__, log_file)
    logger.info('Writing data to file: {}'.format(output_file))
    with open(output_file, newline='') as _to:
        for line in output_data:
            _to.writerow(line.join(','))

def parse_arguments():
    parser = ap.ArgumentParser(description="Writes CSV data matrix to a file.")

    parser.add_argument('file_name', help='Output data file name.')
    parser.add_argument('input_data', help='Data to write.')

    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    write_csv_file(args.file_name, args.input_data, args.log_file)
