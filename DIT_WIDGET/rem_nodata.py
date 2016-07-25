import sys
import getopt

import common.readwrite as io
import common.definitions as d


def remove_null(infile, outfile):
    """Remove records with no data from the dataset."""
    data = io.pull(infile, str)

    out = []
    keep = False
    for row in data:
        for item in row:
            if (item not in d.missing_values):
                keep = True
                break
        if (keep):
            out.append(''.join(row))
            keep = False

    io.push(out, outfile)


def parse_args(args):
    def help():
        print 'remove_null.py -i <input file> -o <output file>'


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
args = parse_args(sys.argv[1:])

count_records(*args)