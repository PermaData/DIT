""" String move for column values. Move in this case means when the pattern
    exists in the indicated column:
    1) removing the pattern from that column
    2) adding the pattern to the other column as indicated
    This script assumes it is receiving a CSV file with 2 columns, the column
    from which to remove and the column to which to add.
"""
import csv
import getopt
import re
import sys

import rill


@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('FROM_REGEX')
@rill.inport('TO_REGEX')
@rill.outport('OUTFILE_OUT')
def move_text(INFILE, OUTFILE_IN, FROM_REGEX, TO_REGEX, OUTFILE_OUT):
    """
    move text within field with new text.
    :param ggd361_csv: input CSV file
    :param out_file: output CSV file
    :param move_from_regex: substring regular expression to move
    :param move_to_regex: substring regular expression to replace
    """
    for infile, outfile, from_regex, to_regex in \
        zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents(),
            FROM_REGEX.iter_contents(), TO_REGEX.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for row in data:
                if is_a_match(move_from_regex, row):
                    new_row = move_pattern(from_regex, to_regex, row)
                    output.writerow(new_row)
                else:
                    output.writerow(row)

    # ofile = open(output_csv, 'w')
    # writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')
    #
    # with open(ggd361_csv) as csv_values:
    #     reader = csv.reader(csv_values, delimiter=',', quoting=csv.QUOTE_NONE)
    #     for row in reader:
    #         if is_a_match(move_from_regex, row):
    #             new_row = move_pattern(move_from_regex, move_to_regex, row)
    #             writer.writerow(new_row)
    #         else:
    #             writer.writerow(row)
    # ofile.close()


def clean_value(value):
    new_value = value.strip().replace('\'', '')
    return new_value


def move_pattern(move_from_regex, move_to_regex, row):
    new_row = []
    for ind, value in enumerate(row):
        new_value = clean_value(value)
        matches = re.match(move_from_regex, clean_value(row[0]))
        if matches and ind == 0:
            new_value = '0'
            if len(matches.groups()) >= 1:
                new_value = matches.group(1)
        elif matches:
            new_value = move_to_regex.replace('.*', clean_value(value))
        new_row.append('\'' + new_value + '\'')
    return new_row


def is_a_match(move_from_regex, row):
    matches = re.match(move_from_regex, clean_value(row[0]))
    return matches is not None
