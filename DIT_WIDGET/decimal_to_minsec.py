#!/usr/bin/python
# -*- coding: utf-8 -*-

import common.readwrite as io
import common.definitions as d


def decimal_to_minsec(infile, outfile):
    data = io.pull(infile, str)

    out=[['', ''] for all in range(len(data))]
    formatstr = '{deg}° {min}" {sec:2.7f}\' {hemi}'
    negatives = ['S', 'W']
    positives = ['N', 'E']
    for row, pair in enumerate(data):
        coordinates = standardize(pair)
        for col, coord in enumerate(coordinates):
            degree = int(coord)
            rm = coord % 1
            minute = int(rm*60)
            rm = (rm*60) % 1
            second = rm*60
            out[row][col] = formatstr.format(deg=abs(degree), min=minute, 
                    sec=second, hemi=negatives[col] if degree < 0 else 
                    positives[col])

    io.push(interpret_out(out), outfile)

    
def standardize(coordstring):
    """Creates a tuple from a standard decimal coordinate string."""
    out = coordstring.replace('°','').replace('W','*-1').replace('S','*-1')
    out = out.replace('N','',).replace('E','')
    return eval(out)
    
def interpret_out(data):
    out = []
    for line in data:
        out.append('{0}, {1}'.format(line[0], line[1]))
    return out