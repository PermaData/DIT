#! /usr/bin/python
# -*- coding: utf-8 -*-
import common.readwrite as io
import common.definitions as d


def minsec_to_decimal(infile, outfile):
    """Convert lat/long coordinates from minutes and seconds to decimal."""

    data = io.pull(infile, str)

    out = []
    for coord in data:
        degrees = int(coord.split('°')[0])
        minutes = int(coord.split("'")[0].split('°')[1])
        seconds = float(coord.split('"')[1])
        degrees += minutes/60. + seconds / 3600
        out.append(degrees)
    io.push(out, outfile)

minsec_to_decimal('COORD.in','COORD.out')