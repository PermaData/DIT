#! /usr/bin/python
import csv

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('UPPER')
@rill.inport('LOWER')
@rill.inport('VALUE')
@rill.outport('OUTFILE_OUT')
def replace_notin_range(INFILE, OUTFILE_IN, UPPER, LOWER, VALUE, OUTFILE_OUT):
    """Replace values not within the range defined by threshold with value within a column file."""
    for infile, outfile, upper, lower, value in zip(INFILE.iter_contents(),
                                                    OUTFILE_IN.iter_contents(),
                                                    UPPER.iter_contents(),
                                                    LOWER.iter_contents(),
                                                    VALUE.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                for i, item in enumerate(line):
                    if (float(item) < lower or float(item) > upper):
                        line[i] = value
                output.writerow(line)

        OUTFILE_OUT.send(outfile)
