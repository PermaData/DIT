"""Counts the number of valid (non-empty) records in a column file."""

import csv

import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('LOGFILE_IN')
@rill.outport('OUTFILE_OUT')
@rill.outport('LOGFILE_OUT')
def count_records(INFILE, OUTFILE_IN, LOGFILE_IN, OUTFILE_OUT, LOGFILE_OUT):
    """Count how many valid records there are."""
    # TODO: This needs to write to a log file
    for infile, outfile, logfile in zip(INFILE.iter_contents(),
                                        OUTFILE_IN.iter_contents(),
                                        LOGFILE_IN.iter_contents()):
        valid_records = 0
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                if not any(item in d.missing_values for item in line):
                    valid_records += 1
            print('Valid Records:', valid_records, file=_log)
            OUTFILE_OUT.send(infile)
            LOGFILE_OUT.send(logfile)
