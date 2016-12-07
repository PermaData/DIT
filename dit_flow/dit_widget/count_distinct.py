"""Counts the number of unique values that occur in a column file OR
Given two columns, counts the number of unique values in column 2 that
    correspond to values in column 1."""

import itertools
import csv

import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('LOGFILE_IN')
@rill.outport('OUTFILE_OUT')
@rill.outport('LOGFILE_OUT')
def count_distinct(INFILE, OUTFILE_IN, LOGFILE_IN, OUTFILE_OUT, LOGFILE_OUT):
    for infile, outfile, logfile in zip(INFILE.iter_contents(),
                               OUTFILE_IN.iter_contents(),
                               LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            N = len(next(data))
            _in.seek(0)

            out = single(data, N)
            print('Number of unique values by column:', out, file=_log)


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
