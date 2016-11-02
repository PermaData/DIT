#! /usr/bin/python
import csv
import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('THRESHOLD')
@rill.inport('VALUE')
@rill.outport('OUTFILE_OUT')
def replace_greater_than(INFILE, OUTFILE_IN, THRESHOLD, VALUE, OUTFILE_OUT):
    """Replace values greater than threshold with value within a column file."""
    for infile, outfile, threshold, value in zip(INFILE.iter_contents(),
                                                 OUTFILE_IN.iter_contents(),
                                                 THRESHOLD.iter_contents(),
                                                 VALUE.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                for i, item in enumerate(line):
                    if (float(item) > threshold):
                        line[i] = value
                output.writerow(line)

        OUTFILE_OUT.send(outfile)
