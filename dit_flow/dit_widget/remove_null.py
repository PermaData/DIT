import csv

import rill
from .common import definitions as d


@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def remove_null(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """Remove records with no data from the dataset."""
    for infile, outfile in zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            keep = False
            for row in data:
                for item in row:
                    try:
                        test = float(item)
                    except ValueError:
                        test = item
                    if (test not in d.missing_values):
                        keep = True
                        break
                if (keep):
                    push.writerow(row)
                    keep = False

        OUTFILE_OUT.send(outfile)
