#! /usr/bin/python

import math
import sys

import common.readwrite as io
import common.definitions as d
import common.parseargs as pa


def statistics(infile, outfile):
    """Calculate and print statistical values of the data."""
    data = io.pull(infile, float)

    filtered = [x for x in data if x not in d.missing_values]

    point_stats = count_points(data)
    distribution = mean_std(filtered)
    minmax = min_max(filtered)

    formatstr = ''
    for i in range(7):
        formatstr += '{' + str(i) + ':0.{p}f},'
    formatstr = formatstr[:-1]  # Remove trailing ,
    out = ['min,max,mean,std,totpts,valid_pts,pts_frac',
           formatstr.format(*(minmax + distribution + point_stats), p=7)]
    io.push(out, outfile)


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


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]

statistics(infile, outfile)
