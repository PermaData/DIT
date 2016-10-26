"""Counts the number of unique values that occur in a column file OR
Given two columns, counts the number of unique values in column 2 that
    correspond to values in column 1."""

import itertools
import csv

from ..rill import rill
from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('MODE')
@rill.outport('OUTFILE_OUT')
def count_values(INFILE, OUTFILE_IN, MODE, OUTFILE_OUT):
    for infile, outfile, mode in zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents(), MODE.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, newline='', 'w') as out:
            data = csv.reader(_in)
            N = len(next(data))
            _in.seek(0)

            if (mode == 'single'):
                out = single(data, N)
                print('Number of unique values by column:', out)
            elif (mode == 'double'):
                out = double(data)


def single(data, N):
    """Count the number of unique values that occur in a data set.
    Inputs:
        data: A csv.reader object that has
        N: the number of columns
    Outputs:
        out: The number of unique values collected
    """
    iterators = itertools.tee(data, N)
    out = [0 for each in range(N)]
    for i, current in enumerate(iterators):
        values = set()
        for line in current:
            values.add(line[i])
        out[i] = len(values)
    return out


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
