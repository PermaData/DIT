import csv

import rill


@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def remove_duplicate(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """Remove duplicate records from the data."""
    for infile, outfile in zip(INFILE.iter_contents(),
                               OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            track = set()
            duplicates = 0
            for row in data:
                test = tuple(row)
                if (test in track):
                    duplicates += 1
                else:
                    track.add(test)
                    output.writerow(row)
            print('Found {0} duplicates'.format(duplicates))

        OUTFILE_OUT.send(outfile)
