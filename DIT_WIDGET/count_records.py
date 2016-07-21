import sys

import common.readwrite as io
import common.parseargs as pa
import common.definitions as d


def count_records(infile, outfile):
    """Count how many valid records there are."""
    data = io.pull(infile, float)

    out = 0
    for val in data:
        if (val not in d.missing_values):
            out += 1

    io.push([out], outfile)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

count_records(infile, outfile)