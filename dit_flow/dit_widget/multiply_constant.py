#! /usr/bin/python
"""Multiplies all numeric values in a column file by a constant."""
import csv

import rill

import common.definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE')
@rill.outport('OUTFILE_OUT')
@rill.inport('CONSTANT')
def mult_const(INFILE, OUTFILE, OUTFILE_OUT, CONSTANT):
    # Multiplies all values in infile by constant and writes the result
    # to outfile.
    for infile, outfile, constant in zip(INFILE.iter_contents(),
                                         OUTFILE_IN.iter_contents(),
                                         CONSTANT.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in, )
            output = csv.writer(_out)
            for line in _in:
                for item in line:
                    if (float(item) not in d.missing_values):
                        value = float(item) * constant

        OUTFILE_OUT.send(outfile)
