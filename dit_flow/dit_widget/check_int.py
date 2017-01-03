"""Checks whether all the values in a column file are integers."""

import csv

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('LOGFILE_IN')
@rill.outport('OUTFILE_OUT')
@rill.outport('LOGFILE_OUT')
def check_int(INFILE, OUTFILE_IN, LOGFILE_IN, OUTFILE_OUT, LOGFILE_OUT):
    """Check whether a value is not an integer."""
    # TODO: This needs to write to the log file
    for infile, outfile, logfile in zip(INFILE.iter_contents(),
                                        OUTFILE_IN.iter_contents(),
                                        LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for i, line in enumerate(data):
                for j, item in enumerate(line):
                    try:
                        value = float(item)
                        if abs(value - round(value)) > 0.000001:
                            print('Row {} column {} has a non-integer value.'.format(i, j), file=_log)
                    except ValueError:
                        print('Row {} column {} has a non-numeric value.'.format(i, j), file=_log)
        OUTFILE_OUT.send(infile)
        LOGFILE_OUT.send(logfile)


    # data = io.pull(infile, float)
    #
    # out = []
    # for (i, val) in enumerate(data):
    #     if (abs(val % 1) > .000000001):
    #         out.append('{0}: {1}'.format(i, val))
    #
    # io.push(out, outfile)
