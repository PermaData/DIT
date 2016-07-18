#! /usr/bin/python

import sys

import common.readwrite as io
import common.definitions as d
import printfamily.prints as p
import common.parseargs as pa


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


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

print_max(infile, outfile)
