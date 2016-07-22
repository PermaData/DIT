#! /usr/bin/python

import sys
import getopt

import common.readwrite as io
import common.definitions as d
import printfamily.prints as p


def print_max(infile, outfile):
    """Prints the maximum and minimum values along with their locations.
    Inputs:
        infile: name of file to read data from
        outfile: name of file to write mins and maxes to
    Outputs:
        Pushes the location and value of maxima and minima to outfile.
    """
    data = io.pull(infile, float)

    # Ignore missing values
    filtered = [x for x in data if x not in d.missing_values]
    mini = min(filtered)
    maxi = max(filtered)

    out = []
    for which, target in enumerate([mini, maxi]):
        out.append(('Location', ['Minimum', 'Maximum'][which]))
        for place, val in enumerate(data):
            if(val == target):
                out.append((place, val))

    rv = p.interpret_out(out)
    rv.insert(0, len(out))

    io.push(rv, outfile)


def parse_args(args):
    def help():
        print 'print_max.py -i <input file> -o <output file>'
        print 'Prints max and mean'


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

    for (option, val) in vals:
        if (option in readoptions[0]):
            infile = val
        elif (option in readoptions[1]):
            outfile = val

    if (any(val is None for val in [infile, outfile])):
        help()
        sys.exit(2)

    return infile, outfile

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])

print_max(*args)
