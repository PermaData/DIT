#! /usr/bin/python

import sys
import math
import getopt

import common.readwrite as io
import common.definitions as d


def print_mean(infile, outfile):
    """Calculates and prints the mean and standard deviation.
    Inputs:
        infile: file to read data from
        outfile: file to write mean and standard deviation to
    Outputs:
        Prints the mean and standard deviation to outfile, with each value
        labeled
        Mean
        #value#
        Standard Deviation
        #value#
    """
    # Read data from infile
    data = io.pull(infile, float)

    # Ignore missing values
    filtered = [x for x in data if x not in d.missing_values.keys()]

    # Calculate statistical values
    values = calculate(filtered)

    # Write to outfile
    io.push(["Mean", '{:0.{p}f}'.format(values[0], p=7), "Standard Deviation",
             '{:0.{p}f}'.format(values[1], p=7)], outfile)


def calculate(data):
    """Calculates the mean and standard deviation of the given data set."""
    # Calculate the mean
    if(len(data) == 0):
        # There is no data
        return (0, 0)
    else:
        mean = sum(data) / len(data)

    variance = 0
    for val in data:
        # Calculate the variance (the sum of squares of residuals)
        variance += (val - mean)**2
    # Take the square root to get standard deviation
    if(len(data) == 1):
        # There is only one data point
        return (mean, 0)
    else:
        std = math.sqrt(variance / (len(data)-1))

    return (mean, std)


def parse_args(args):
    def help():
        print 'print_mean.py -i <input file> -o <output file>'
        print 'Prints mean and standard deviation'


    infile = None
    outfile = None

    options = ('i:o:',
               ['input', 'output'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, val) in vals:
        if (option in readoptions[0]):
            infile = val
        elif (option in readoptions[1]):
            outfile = val

    if (any(val is None for val in [infile, outfile])):
        help()
        sys.exit(2)

    return infile, outfile


args = parse_args(sys.argv[1:])

print_mean(*args)