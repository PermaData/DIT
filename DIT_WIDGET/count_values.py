import common.readwrite as io
import common.parseargs as pa
import common.definitions as d


def count_values(infile, outfile, mode='single'):
    data = io.pull(infile, float)

    out = single(data)

    io.push(out, outfile)


def single(data):
    values = {}  # Maps value:number of occurrences
    for item in data:
        if (item not in values and item not in d.missing_values):
            values[item] = 1
        else:
            values[item] += 1
    out = [len(values)]
    for key in sorted(values.keys()):
        out.append('{0:0.7f}: {1}'.format(key, values[key]))


def double(data):
    values = {{}}
    for item in data:
        pass


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

count_values(infile, outfile)