#! /usr/bin/python

import sys

import mathfamily.arithmetic as a
import common.parseargs as pa


def sub_const(infile, outfile, constant):
    # Subtracts constant from all values in infile and writes the result
    # to outfile.
    a.arithmetic(infile, outfile, constant, lambda x, y: x-y,
                 lambda x, y: False)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
constant = args[2][0]

sub_const(infile, outfile, constant)
