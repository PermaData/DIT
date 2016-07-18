#! /usr/bin/python

import sys

import printfamily.prints as p
import common.parseargs as pa


def print_gt(infile, outfile, num):
    """Print all values greater than a threshold."""
    p.print_conditional(infile, outfile, num, lambda x, y: x > y)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]

print_gt(infile, outfile, threshold)
