#!/usr/bin/python
"""Adds a constant to all numeric values in a column file."""
import csv

def add_constant(constant, missing_value, infile, outfile, logfile):
    # Adds constant to all values in infile and writes the result to
    # outfile.
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

    return [outfile, logfile]
