#! /usr/bin/python
"""Divides all numeric values in a column file by a constant."""
import csv
import shutil

import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('LOGFILE_IN')
@rill.inport('CONSTANT')
@rill.outport('OUTFILE_OUT')
@rill.outport('LOGFILE_OUT')
def divide_constant(INFILE, OUTFILE_IN, LOGFILE_IN, CONSTANT, OUTFILE_OUT, LOGFILE_OUT):
    # Adds constant to all values in infile and writes the result to
    # outfile.
    for infile, outfile, constant, logfile in zip(INFILE.iter_contents(),
                                                  OUTFILE_IN.iter_contents(),
                                                  CONSTANT.iter_contents(),
                                                  LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            output = csv.writer(_out)
            if (constant == 0):
                # Can't divide by zero, just copy the whole thing unchanged
                shutil.copy2(infile, outfile)
            else:
                for line in data:
                    modified = line
                    for i, item in enumerate(line):
                        item = item.strip("'")
                        if (float(item) not in d.missing_values):
                            modified[i] = float(item) / constant
                    output.writerow(modified)

        OUTFILE_OUT.send(outfile)
        LOGFILE_OUT.send(logfile)
