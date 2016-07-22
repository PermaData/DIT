import re
import sys

import common.readwrite as io
import common.parseargs as pa
import common.definitions as d


def remove_chars(infile, outfile, chars):
    """Remove all from a set of characters from a column."""
    data = io.pull(infile, str)

    pun = '[' + chars + ']'
    out = []
    for s in data:
        out.append(re.sub(pun, '', s))
    io.push(out, outfile)


def parse_args(args):
    def help():
        print 'remove_chars.py -i <input file> -o <output file> -c <characters to remove>'


    infile = None
    outfile = None
    chars = None

    options = ('i:o:c:',
               ['input', 'output', 'chars'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, value) in vals:
        if (option in readoptions[0]):
            infile = value
        elif (option in readoptions[1]):
            outfile = value
        elif (option in readoptions[2]):
            chars = value

    if (any(val is None for val in [infile, outfile, chars])):
        help()
        sys.exit(2)

    return infile, outfile, chars
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])
# infile = args[0]
# outfile = args[1]
# chars = args[3][0]

remove_chars(*args)