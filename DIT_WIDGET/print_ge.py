#! /usr/bin/python

import sys

import printfamily.prints as p
import common.parseargs as pa


def print_ge(infile, outfile, num):
    """Print all values greater than or equal to a threshold."""
    p.print_conditional(infile, outfile, num, lambda x, y: x >= y)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]

print_ge(infile, outfile, threshold)
