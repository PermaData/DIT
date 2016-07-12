#! /usr/bin/python

import sys

import replacefamily.replacements as r
import common.parseargs as pa


def replace_notin_rangex(infile, outfile, threshold, value):
    r.replace_conditional(infile, outfile, threshold, value,
                          lambda x, y: x < y[0] or x > y[1])


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
threshold = (args[2][0], args[2][1])
value = args[2][2]

replace_notin_rangex(infile, outfile, threshold, value)
