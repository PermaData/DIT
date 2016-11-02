#! /usr/bin/python
"""Calculates a probability density function of the numeric data in a column file."""

import csv

import rill

from .common import definitions as d


@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('BINS')
@rill.inport('MINMAX')
@rill.inport('LOWER')
@rill.inport('UPPER')
@rill.inport('OUTLIERS')
@rill.inport('NORM')
@rill.outport('OUTFILE_OUT')
def pdf(INFILE, OUTFILE_IN, BINS, MINMAX, LOWER, UPPER, OUTLIERS, NORM, OUTFILE_OUT):
    """Create a probability density function of the data in infile.
    It can only deal with a single column of data at this time.
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
    for infile, outfile, bins, minmax, lower, upper, outliers, norm in \
        zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents(),
            BINS.iter_contents(), MINMAX.iter_contents(),
            LOWER.iter_contents(), UPPER.iter_contents(),
            OUTLIERS.iter_contents(), NORM.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, 'w', newline='') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)

            # The function may be called without options being explicitly passed
            if(norm in d.missing_values):
                norm = 'raw'
            if(minmax in d.missing_values):
                minmax = 'auto'
            if(outliers in d.missing_values):
                outliers = 'exclude'

            bins = int(bins)

            # Look only at valid data
            # filtered = [x for x in data if x not in d.missing_values]
            # filtered = filter(lambda line: (line[0] not in d.missing_values), data)
            filtered = []
            for line in data:
                try:
                    item = float(line[0])
                except ValueError:
                    continue
                if item not in d.missing_values:
                    filtered.append(item)

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
                print("Use a valid form for the minmax argument")
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
                        # beyond the end, because of error inherent in
                        # floating-point approximation
                        out[-1].append(val)
                else:
                    # Error with the outlier option
                    print("Use a valid form for the outlier argument")
                    return None

            norms = {'raw': raw,
                     'probability': probability
                     }
            if(norm not in norms):
                # Error with the norm option
                print("Use a valid form for the norm argument")
                return None

            out = norms[norm](out)

            out.insert(0, 'Minimum: {0}'.format(mini))
            out.append('Maximum: {0}'.format(maxi))

            for row in out:
                print(row)

        OUTFILE_OUT.send(infile)


def raw(data):
    # Return the number of data points that fall in each bin
    return [len(group) for group in data]


def probability(data):
    # Return the relative probabilities of the bins
    npoints = sum(raw(data))
    return [float(len(group)) / npoints for group in data]
