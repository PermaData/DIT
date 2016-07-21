import sys

import common.readwrite as io
import common.parseargs as pa
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
        out.append('{0:0.7f}: {1}'.format(float(key), len(values[key])))
    return out


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
try:
    mode = args[3][0]
except IndexError:
    # no mode was given explicitly
    mode = 'single'

count_values(infile, outfile, mode)