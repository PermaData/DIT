import sys
import getopt

import common.readwrite as io
import common.definitions as d

__all__ = ['type_conversion']


def type_conversion(infile, outfile, mode):
    data = io.pull(infile, str)

    input_map = {'str': cast_str, 'string': cast_str,
                 'int': cast_int, 'integer': cast_int,
                 'float': cast_float, 'real': cast_float,
                 }
    conv = input_map[mode.lower()]

    out = [[conv(item) for item in row] for row in data]

    io.push(out, outfile)


def cast_int(value):
    return int(float(value))

def cast_float(value):
    return float(value)

def cast_str(value):
    return str(value)


def parse_args(args):
    def help():
        print 'type_conversion.py -i <input file> -o <output file> -m <mode>'


    infile = None
    outfile = None
    mode = None

    options = ('i:o:m:', ['input', 'output', 'mode'])
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
            mode = value

    if (any(val is None for val in [infile, outfile, mode])):
        help()
        sys.exit(2)

    return infile, outfile, mode

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
if (__name__ == '__main__'):
    args = parse_args(sys.argv[1:])

    type_conversion(*args)