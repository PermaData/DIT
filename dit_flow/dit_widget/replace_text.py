""" String replace for column values. """
import csv
import getopt
import sys
import re

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('TO_REPLACE')
@rill.inport('WITH_REPLACE')
@rill.outport('OUTFILE_OUT')
def replace_text(INFILE, OUTFILE_IN, TO_REPLACE, WITH_REPLACE, OUTFILE_OUT):
    """
    Replace text within field with new text.
    :param ggd361_csv: input CSV file
    :param out_file: output CSV file
    :param to_replace: substring within field to be replaced
    :param with_replace: substring to replace to_replace substring
    """
    for infile, outfile, to_replace, with_replace in \
        zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents(),
            THRESHOLD.iter_contents(), VALUE.iter_contents()):
        with open(infile) as _in, open(outfile, 'w') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for row in data:
                for i, item in enumerate(row):
                    field = item.replace("'", "")
                    new_field = re.sub(to_replace, with_replace, field)
                    row[i] = "'{0}'".format(new_field)
                output.writerow(row)

    # ofile = open(out_file, 'w')
    # writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')
    #
    # csv_data = []
    # field_names = None
    # with open(ggd361_csv) as csv_values:
    #     reader = csv.reader(csv_values, delimiter=',', quoting=csv.QUOTE_NONE)
    #     for row in reader:
    #         field = row[0].replace('\'', '')
    #         new_field = field.replace(to_replace, with_replace)
    #         row[0] = '\'' + new_field + '\''
    #
    #         writer.writerow(row)
    # ofile.close()
