#! /usr/bin/python

import sys

import replacefamily.replacements as r
# import common.parseargs as pa


def replace_ge(infile, outfile, threshold, value):
    r.replace_conditional(infile, outfile, threshold, value,
                          lambda x, y: x >= y)


def parse_args(args):
    def help():
        print 'replace_ge.py -i <input file> -o <output file> -t <threshold> -v <replacement value>'
        print 'Replaces values greater than or equal to threshold with replacement'



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

    if (any(val is None for val in
            [infile, outfile, threshold, value])):
        help()
        sys.exit(2)

    return infile, outfile, threshold, value
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])
# infile = args[0]
# outfile = args[1]
# threshold = args[2][0]
# value = args[2][1]

replace_ge(*args)
