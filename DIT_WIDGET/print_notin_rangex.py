#! /usr/bin/python

import sys

import printfamily.prints as p
import common.parseargs as pa


def print_notin_rangex(infile, outfile, num):
    """Prints all values outside of two thresholds."""
    p.print_conditional(infile, outfile, num,
                        lambda x, y: x < y[0] or x > y[1])


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]

print_le(infile, outfile, threshold)
