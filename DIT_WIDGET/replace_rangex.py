#! /usr/bin/python

import sys

import replacefamily.replacements as r
import common.parseargs as pa


def replace_rangex(infile, outfile, threshold, value):
    r.replace_conditional(infile, outfile, threshold, value,
                          lambda x, y: x > y[0] and x < y[1])


def parse_args(args):
    def help():
        print 'replace_rangex.py -i <input file> -o <output file> -z <zone column index> -e <easting column index> -n <northing column index> [-h <hemisphere>]\nCheck that your argument list is correct.'


    infile = None
    outfile = None
    zone_col = None
    east_col = None
    north_col = None

    hemisphere = 'north'

    options = ('i:o:z:e:n:h:',
                ['input', 'output', 'zone_index', 'easting_index',
                'northing_index', 'hemisphere'])
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
        elif (option in readoptions[2]):
            zone_col = int(value)
        elif (option in readoptions[3]):
            east_col = int(value)
        elif (option in readoptions[4]):
            north_col = int(value)
        elif (option in readoptions[5]):
            hemisphere = value

    if (any(val is None for val in
            [infile, outfile, zone_col, east_col, north_col])):
        help()
        sys.exit(2)

    return infile, outfile, zone_col, east_col, north_col, hemisphere
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = (args[2][0], args[2][1])
value = args[2][2]

replace_rangex(infile, outfile, threshold, value)
