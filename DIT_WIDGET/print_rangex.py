#! /usr/bin/python

import sys

import printfamily.prints as p
import common.parseargs as pa


def print_rangex(infile, outfile, num):
    """Prints all values between two thresholds.
    """
    p.print_conditional(infile, outfile, num,
                        lambda x, y: x > y[0] and x < y[1])


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]

print_le(infile, outfile, threshold)
