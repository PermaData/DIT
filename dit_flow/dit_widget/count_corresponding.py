import itertools
import csv

import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def count_corresponding(INFILE, OUTFILE_IN, OUTFILE_OUT):
    for infile, outfile in zip(INFILE.iter_contents(),
                               OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)

            out = double(data)
            print('Primary Value: Number of secondary values')
            for item in out:
                print(item)


def double(data):
    """Count the number of unique values of one data set matched with another.
    Inputs:
        data: A csv.reader object to a file with two columns. The first
            column is assumed to be the primary.
    Outputs:
        out: A list of strings showing primary value: number of
            secondary values
    """
    values = {}  # Maps value: set of occurrences
    for first, second in data:
        if (first not in values and first not in d.missing_values):
            values[first] = set([second])
        else:
            values[first].add(second)
    # out = [len(values)]
    out = []
    for key in sorted(values.keys()):
        out.append('{0}: {1}'.format(key, len(values[key])))
    return out
