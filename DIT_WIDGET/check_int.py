import sys
import getopt

import common.readwrite as io
# import common.parseargs as pa


def check_ints(infile, outfile):
    """Check whether a value is not an integer."""
    data = io.pull(infile, float)

    out = []
    for (i, val) in enumerate(data):
        if (abs(val%1) > .000000001):
            out.append('{0}: {1}'.format(i, val))

    io.push(out, outfile)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

check_ints(infile, outfile)