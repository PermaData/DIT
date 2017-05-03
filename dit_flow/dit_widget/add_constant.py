#!/usr/bin/python
"""Adds a constant to all numeric values in a column file."""
import csv

#import common.definitions as d


def add_constant(INFILE, OUTFILE_IN, LOGFILE_IN, CONSTANT, OUTFILE_OUT,
                 LOGFILE_OUT):
    # Adds constant to all values in infile and writes the result to
    # outfile.
    for infile, outfile, constant, logfile in zip(INFILE.iter_contents(),
                                                  OUTFILE_IN.iter_contents(),
                                                  CONSTANT.iter_contents(),
                                                  LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out, \
             open(logfile, 'a') as _log:
            print('Adding {} to the column'.format(constant), file=_log)
            data = csv.reader(_in, )
            output = csv.writer(_out)
            for line in _in:
                for item in line:
                    if (float(item) not in [-10]): #d.missing_values):
                        value = float(item) + constant

        OUTFILE_OUT.send(outfile)
        LOGFILE_OUT.send(logfile)
