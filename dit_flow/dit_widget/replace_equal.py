#! /usr/bin/python
import csv

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
@rill.inport('TARGET')
@rill.inport('VALUE')
def replace_equal(INFILE, OUTFILE_IN, OUTFILE_OUT, TARGET, VALUE):
    """Replace values equal to threshold with value within a column file."""
    for infile, outfile, target, value in zip(INFILE.iter_contents(),
                                              OUTFILE_IN.iter_contents(),
                                              TARGET.iter_contents(),
                                              VALUE.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                for i, item in enumerate(line):
                    if (float(item) == target):
                        line[i] = value
                output.writerow(line)

        OUTFILE_OUT.send(outfile)
