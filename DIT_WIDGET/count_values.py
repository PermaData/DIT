import common.readwrite as io


def count_values(infile, outfile):
    data = io.pull(infile, float)
    
    values = {}  # Maps value:number of occurrences
    for item in data:
        if (item not in values):
            values[item] = 1
        else:
            values[item] += 1
    out = [len(values)]
    for key in sorted(values.keys()):
        out.append('{0}: {1}'.format(key, values[key]))
    
    io.push(out, outfile)