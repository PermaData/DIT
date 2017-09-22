import csv

from dit_flow.dit_widget.common.setup_logger import setup_logger


def read_csv_file(file_name, log_file=None):
    logger = setup_logger(__name__, log_file)
    logger.info('Reading file: {}'.format(file_name))
    data = []
    with open(file_name, newline='') as _from:
        count = []
        data_reader = csv.reader(_from, quoting=csv.QUOTE_NONE, quotechar="'")
        for line in data_reader:
            data.append(line)
            count.append(len(line))
        try:
            isOK = column_check(count, logger)
        except IOError as e:
            logger.error(e)
            isOK = False

    if (isOK):
        return data
    else:
        return None


def column_check(count, logger):
    mean = round(float(sum(count)) / len(count))
    error = False
    for (i, item) in enumerate(count):
        if (item != mean):
            logger.error('Line {0} has a different number of columns than the'
                         'rest of the file.'.format(i + 1))
            error = True
    if (error):
        raise IOError('One or more of the lines was flawed.')
    else:
        return True

def parse_arguments():
    parser = ap.ArgumentParser(description="Reads input CSV file and returns data matrix.")

    parser.add_argument('file_name', help='Input data file.')

    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    read_csv_file(args.file_name, args.log_file)
