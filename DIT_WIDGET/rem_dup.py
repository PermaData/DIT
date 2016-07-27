import sys
import getopt

import common.readwrite as io
import common.definitions as d

__all__ = ['remove_duplicate']


def remove_duplicate(infile, outfile):
    """Remove duplicate records from the data."""
    data = io.pull(infile, str)

    records = set()
    for row in data:
        # Rejoin the line into a string for set insertion
        # A somewhat regrettable extra step
        record = ''.join(row)
        records.add(record)
    out = sorted(records)

    io.push(out, outfile)


def parse_args(args):
    def help():
        print 'remove_duplicate.py -i <input file> -o <output file>'


    infile = None
    outfile = None

    options = ('i:o:',
               ['input', 'output'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, value) in vals:
        if (option in readoptions[0]):
            infile = value
        elif (option in readoptions[1]):
            outfile = value

    if (any(val is None for val in [infile, outfile])):
        help()
        sys.exit(2)

    return infile, outfile

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
if (__name__ == '__main__'):
    args = parse_args(sys.argv[1:])

    remove_duplicate(*args)