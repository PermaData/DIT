import math
import csv

import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def statistics(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """Calculate and print statistical values of the data."""
    for infile, outfile in zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            filtered = []
            for line in data:
                try:
                    item = float(line[0])
                except ValueError:
                    continue
                if item not in d.missing_values:
                    filtered.append(item)
            point_stats = count_points(data)
            distribution = mean_std(filtered)
            minmax = min_max(filtered)
            out = []
            names = ['Min', 'Max', 'Mean', 'Standard Deviation', 'Total points',
                     'Valid points', 'Valid fraction']
            formatstr = '{0}: {1:0.{p}f}'
            for name, value in zip(names, minmax + distribution + point_stats):
                out.append(formatstr.format(name, value, p=7))

            for s in out:
                print(s)
        OUTFILE_OUT.send(infile)

# Helper functions

#   This one is passed the unfiltered data

def count_points(rawdata):
    total = 0
    valid = 0
    for point in rawdata:
        total += 1
        if(point not in d.missing_values):
            valid += 1

    return (total, valid, float(valid) / total)


#   These are passed the filtered data


def mean_std(data):
    """Calculates the mean and standard deviation of the given data set."""
    # Calculate the mean
    if(len(data) == 0):
        return (0, 0)
    else:
        mean = sum(data) / len(data)
    variance = 0
    for val in data:
        # Calculate the variance (the sum of squares of residuals)
        variance += (val - mean)**2
    # Take the square root to get standard deviation
    if(len(data) <= 1):
        return (mean, 0)
    else:
        std = math.sqrt(variance / (len(data)-1))
    return (mean, std)


def min_max(data):
    return (min(data), max(data))


def median(data):
    data.sort()
    if(len(data) % 2 == 1):
        # Return the center of the sorted list
        return data[len(data) // 2 + 1]
    else:
        # Return the mean of the two center values
        return (data[len(data) // 2] + data[len(data) // 2 + 1]) / 2
