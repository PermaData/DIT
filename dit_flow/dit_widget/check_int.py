"""Checks whether all the values in a column file are integers."""

import csv

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE')
@rill.outport('OUTFILE_OUT')
def check_ints(INFILE, OUTFILE, OUTFILE_OUT):
    """Check whether a value is not an integer."""
    # TODO: This needs to write to the log file
    for infile, outfile in zip(INFILE.iter_contents(), OUTFILE.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for i, line in enumerate(data):
                for j, item in enumerate(line):
                    try:
                        value = float(item)
                        if abs(value - round(value)) > 0.000001:
                            print('Row {} column {} has a non-integer value.'.format(i, j))
                    except ValueError:
                        print('Row {} column {} has a non-integer value.'.format(i, j))
        OUTFILE_OUT.send(infile)


    # data = io.pull(infile, float)
    #
    # out = []
    # for (i, val) in enumerate(data):
    #     if (abs(val % 1) > .000000001):
    #         out.append('{0}: {1}'.format(i, val))
    #
    # io.push(out, outfile)
