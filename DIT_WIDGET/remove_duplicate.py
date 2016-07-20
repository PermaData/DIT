import sys

import common.readwrite as io
import common.parseargs as pa
import common.definitions as d


def remove_duplicate(infile, outfile):
    """ """
    data = io.pull(infile, float)

    

    io.push([out], outfile)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

remove_duplicate(infile, outfile)