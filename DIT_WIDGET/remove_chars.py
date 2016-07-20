import re

import common.readwrite as io
import common.parseargs as pa
import common.definitions as d


def remove_chars(infile, outfile, chars):
    """Count how many valid records there are."""
    data = io.pull(infile, str)

    pun = '[' + chars + ']'
    out = []
    for s in data:
        out.append(re.sub(pun, '', s))

    io.push([out], outfile)


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
chars = args[3][0]

remove_chars(infile, outfile, chars)