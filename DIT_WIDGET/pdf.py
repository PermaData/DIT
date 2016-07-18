#! /usr/bin/python
import sys

import common.readwrite as io
import common.definitions as d
import common.parseargs as pa


def pdf(infile, outfile, bins, minmax, lower, upper, outliers, norm):
    """Create a probability density function of the data in infile.
    Inputs:
        infile: the file to read data from
        outfile: the file to write data to
        bins: the number of bins to sort data into
        minmax: If 'auto', sets the range of the distribution to be the
            entire range of the data set. If 'manual', sets the range to
            be defined by [lower, upper].
        outliers: If 'exclude', ignore values that fall outside the
            range. If 'include', values outside the range will be sorted
            into the tail bins.
        norm: If 'raw', returns the number of values that fall in each
            bin. If 'probability', returns the proportion of values that
            fall in each bin.
    Outputs:
        Writes a vector of bin values as determined by the 'norm'
        argument to outfile.
    """

    # The function may be called without options being explicitly passed
    if(norm in d.missing_values):
        norm = 'raw'
    if(minmax in d.missing_values):
        minmax = 'auto'
    if(outliers in d.missing_values):
        outliers = 'exclude'

    data = io.pull(infile, float)

    bins = int(bins)

    # Look only at valid data
    filtered = [x for x in data if x not in d.missing_values]

    if(minmax == 'auto'):
        mini = min(filtered)
        maxi = max(filtered)
        val_range = maxi - mini
    elif(minmax == 'manual'):
        mini = lower
        maxi = upper
        val_range = upper - lower
    else:
        # Error with the minmax option
        print "Use a valid form for the minmax argument"
        return None

    out = [[] for each in range(bins)]
    for val in filtered:
        # Calculate which bin the value should go in.
        loc = ((val - mini) * bins) / val_range
        loc = int(loc)

        if(outliers == 'include'):
            if(loc < 0):
                # The value is below the lower limit on range
                loc = 0
            elif(loc >= bins):
                # The value is above the upper range limit
                loc = bins - 1
            out[loc].append(val)  # Place the value in the bin
        elif(outliers == 'exclude'):
            if(loc >= 0 and loc < bins):
                out[loc].append(val)
            elif(val == maxi):
                # The maximum value is sometimes sorted into the bin
                # beyond the end
                out[-1].append(val)
        else:
            # Error with the outlier option
            print "Use a valid form for the outlier argument"
            return None

    norms = {'raw': raw,
             'probability': probability
             }
    if(norm not in norms):
        # Error with the norm option
        print "Use a valid form for the norm argument"
        return None

    # Push the correct data to outfile
    io.push(norms[norm](out), outfile)


def raw(data):
    # Return the number of data points that fall in each bin
    return [len(group) for group in data]


def probability(data):
    # Return the relative probabilities of the bins
    npoints = sum(raw(data))
    return [float(len(group)) / npoints for group in data]


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
bins = args[2][0]
minmax = args[3][0]
if(minmax == 'manual'):
    lower = args[2][1]
    upper = args[2][2]
else:
    lower = upper = 0
outliers = args[3][1]
norm = args[3][2]

pdf(infile, outfile, bins, minmax, lower, upper, outliers, norm)
