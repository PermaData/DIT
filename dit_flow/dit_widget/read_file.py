import csv

from dit_flow.dit_widget.common.setup_logger import setup_logger

def read_file(name, id, log_file=None):
    logger = setup_logger(self.__name__, log_file)
    logger.info("args: ", name, "  ", id, "  ", log_file)
    path, base = name.rsplit('/', 1)
    main_name = '{pth}/{id}_In_{base}.csv'.format(pth=path, id=id,
                                                  base=base)
    with open(name, newline='') as _from, \
         open(main_name, 'w', 0o666, newline='') as _to:
        data = csv.reader(_from, quoting=csv.QUOTE_NONNUMERIC,
                          quotechar="'")
        try:
            isOK = column_check(data)
        except IOError as e:
            with open(log_file, 'a') as log:
                print(e, file=log)
            isOK = False
        _from.seek(0)
        output = csv.writer(_to, quoting=csv.QUOTE_NONNUMERIC,
                            quotechar="'")
        # Copies the data into the file that will be base input from now on
        for line in data:
            output.writerow(line)

    if (isOK):
        return data
    else:
        return None


def column_check(data):
    # TODO: Check if this exhausts the iterator in containing scope
    # NOTE: It does, you need to reset with a seek(0) command
    # TODO: Pass in the log file so errors can be saved for later inspection
    """Expects a csv.reader object."""
    count = []
    for line in data:
        count.append(len(line))
    mean = round(float(sum(count)) / len(count))
    error = False
    for (i, item) in enumerate(count):
        if (item != mean):
            print('Line {0} has a different number of columns than the rest '
                  'of the file.'.format(i + 1))
            error = True
    if (error):
        raise IOError('One or more of the lines was flawed.')
    else:
        return True

    def parse_arguments():
        parser = ap.ArgumentParser(description="Adds constant to all values in " \
                                               "input_data_file and writes the result to " \
                                               "output_data_file.")

        parser.add_argument('name', help='Input data file.')
        parser.add_argument('id', type=int, help='Step ID.')

        parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

        return parser.parse_args()

    if __name__ == '__main__':
        args = parse_arguments()

        read_file(args.name, args.id, args.log_file)
