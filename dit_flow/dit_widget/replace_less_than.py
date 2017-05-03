#! /usr/bin/python
import csv

from circuits import Component

class ReplaceLessThan(Component):

    channel = 'ReplaceLessThan'

    def go(self, event):
        print(self.channel, ' received go event')

def replace_less_than(INFILE, OUTFILE_IN, LOGFILE_IN, THRESHOLD, VALUE, OUTFILE_OUT, LOGFILE_OUT):
    """Replace values less than threshold with value within a column file."""
    for infile, outfile, threshold, value, logfile in zip(INFILE.iter_contents(),
                                                 OUTFILE_IN.iter_contents(),
                                                 THRESHOLD.iter_contents(),
                                                 VALUE.iter_contents(),
                                                 LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                for i, item in enumerate(line):
                    if (float(item) < threshold):
                        line[i] = value
                output.writerow(line)

        OUTFILE_OUT.send(outfile)
        LOGFILE_OUT.send(logfile)
