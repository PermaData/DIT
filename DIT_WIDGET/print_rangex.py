#! /usr/bin/python

import sys

import printfamily.prints as p
import common.parseargs as pa


def print_rangex(infile, outfile, num):
    """Prints all values between two thresholds.
    """
    p.print_conditional(infile, outfile, num,
                        lambda x, y: x > y[0] and x < y[1])


def parse_args(args):
    def help():
        print 'replace_le.py -i <input file> -o <output file> -t <threshold> -v <replacement value>'
        print 'Replaces values less than threshold with replacement'


    infile = None
    outfile = None
    threshold = None
    value = None

    options = ('i:o:t:v:',
                ['input', 'output', 'threshold', 'value'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, val) in vals:
        if (option in readoptions[0]):
            infile = val
        elif (option in readoptions[1]):
            outfile = val
        elif (option in readoptions[2]):
            threshold = int(val)
        elif (option in readoptions[3]):
            value = int(val)

    if (any(val is None for val in [infile, outfile, threshold, value])):
        help()
        sys.exit(2)

    return infile, outfile, threshold, value
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]

print_le(infile, outfile, threshold)
