#!/usr/bin/python
import csv

from ..rill import rill

from .common import definitions as d


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE')
@rill.outport('OUTFILE_OUT')
def decimal_to_minsec(INFILE, OUTFILE, OUTFILE_OUT):
    # TODO: add missing value functionality

    f = open(infile)
    data = f.readlines()

    out = [['', ''] for all in range(len(data))]
    formatstr = '{deg:03.0f}\xb0 {min:02.0f}\' {sec:02.0f}" {hemi}'
    negatives = ['S', 'W']
    positives = ['N', 'E']
    for row, pair in enumerate(data):
        coordinates = standardize(pair.strip())
        for col, coord in enumerate(coordinates):
            degree = int(coord)
            rm = abs(coord) % 1
            minute = int(rm * 60)
            rm = (rm * 60) % 1
            second = rm * 60
            out[row][col] = formatstr.format(deg=abs(degree), min=minute,
                    sec=second, hemi=negatives[col] if degree < 0 else
                    positives[col])

    io.push(interpret_out(out), outfile)


def standardize(coordstring):
    """Creates a tuple from a standard decimal coordinate string."""
    out = coordstring.replace('\xb0', '').replace('W', '*-1').replace('S', '*-1')
    out = out.replace('N', '').replace('E', '')
    return eval(out)


def interpret_out(data):
    out = []
    for line in data:
        out.append('{0}, {1}'.format(line[0], line[1]))
    return out
