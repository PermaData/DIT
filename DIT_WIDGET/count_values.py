import sys
import getopt

import common.readwrite as io
import common.definitions as d


def count_values(infile, outfile, mode='single'):
    data = io.pull(infile, str)

    if (mode == 'single'):
        out = single(data)
    elif (mode == 'double'):
        out = double(data)

    io.push(out, outfile)


def single(data):
    values = set()  # Maps value: number of occurrences
    for item in data:
        values.add(item)
    out = [len(values)]
    return out


def double(data):
    """Takes a list of 2-element row lists."""
    values = {}  # Maps value: set of occurrences
    for first, second in data:
        if (first not in values and first not in d.missing_values):
            values[first] = set([second])
        else:
            values[first].add(second)
    out = [len(values)]
    for key in sorted(values.keys()):
        out.append('{0}: {1}'.format(key, len(values[key])))
    return out

    
def parse_args(args):
    def help():
        print 'count_values.py -i <input file> -o <output file> [-m <mode>]\nCheck that your argument list is correct.'


    infile = None
    outfile = None
    
    mode = 'single'

    options = ('i:o:m:',
                ['input', 'output', 'mode'])
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

    if (any(val is None for val in [infile, outfile])):
        help()
        sys.exit(2)

    return infile, outfile, mode

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])

count_values(*args)