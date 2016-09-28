""" String replace for column values. """
import csv
import getopt
import sys


def replace_text(ggd361_csv, out_file, to_replace, with_replace):
    """
    Replace text within field with new text.
    :param ggd361_csv: input CSV file
    :param out_file: output CSV file
    :param to_replace: substring within field to be replaced
    :param with_replace: substring to replace to_replace substring
    """
    ofile = open(out_file, 'w')
    writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')

    csv_data = []
    field_names = None
    with open(ggd361_csv) as csv_values:
        reader = csv.reader(csv_values, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            field = row[0].replace('\'', '')
            new_field = field.replace(to_replace, with_replace)
            row[0] = '\'' + new_field + '\''

            writer.writerow(row)
    ofile.close()


def parse_arguments(argv):
    """ Parse the command line arguments and return them. """
    ggd361_csv = None
    out_file = None
    to_replace = None
    with_replace = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:t:w:", ["ggd361_csv=", "out_file=", "to_replace=", "with_replace="])
    except getopt.GetoptError:
        print('replace_text.py -i <GGD361 CSV file> -o <CSV output file> -t <text in field to replace> -w <replacement text>')
        sys.exit(2)

    found_in_file = False
    found_out_file = False
    found_to_replace = False
    found_with_replace = False
    for opt, arg in opts:
        if opt == '-h':
            print('replace_text.py -i <GGD361 CSV file> -o <CSV output file> -t <text in field to replace> -w <replacement text>')
            sys.exit()
        elif opt in ("-i", "--ggd361_csv"):
            found_in_file = True
            ggd361_csv = arg
        elif opt in ("-o", "--out_file"):
            found_out_file = True
            out_file = arg
        elif opt in ("-t", "--to_replace"):
            found_to_replace = True
            to_replace = arg
        elif opt in ("-w", "--with_replace"):
            found_with_replace = True
            with_replace = arg
    if not found_in_file:
        print("Input file '-i' argument required.")
        sys.exit(2)
    if not found_out_file:
        print("Output file '-o' argument required.")
        sys.exit(2)
    if not found_to_replace:
        print("Text within field to replace '-t' argument required.")
        sys.exit(2)
    if not found_with_replace:
        # print "Replacement text '-w' argument required."
        # sys.exit(2)
        with_replace = ''
    return (ggd361_csv, out_file, to_replace, with_replace)


if __name__ == '__main__':
    (ggd361_csv, output_csv, to_replace, with_replace) = parse_arguments(sys.argv[1:])

    replace_text(ggd361_csv.strip(), output_csv.strip(), to_replace.strip(), with_replace.strip())
