#!/usr/bin/python
# -*- coding: utf-8 -*-

import common.readwrite as io
import common.definitions as d


def decimal_to_minsec(infile, outfile):
    data = io.pull(infile)

    out=[('','') for all in range(len(data))]
    formatstr = '{deg}° {min}" {sec:2.4f}\''
    for row, pair in enumerate(data):
        for col, coord in enumerate(pair):
            degree = int(coord)
            rm = coord % 1
            minute = int(rm*60)
            rm = (rm*60) % 1
            second = rm*60
            out[row][col] = formatstr.format(deg=degree, min=minute, sec=second)
    return out
