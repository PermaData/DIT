#! /usr/bin/python

import sys

import replacefamily.replacements as r
import common.parseargs as pa


def replace_eq(infile, outfile, threshold, value):
    r.replace_conditional(infile, outfile, threshold, value,
                          lambda x, y: x == y)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = args[2][0]
value = args[2][1]

replace_eq(infile, outfile, threshold, value)
