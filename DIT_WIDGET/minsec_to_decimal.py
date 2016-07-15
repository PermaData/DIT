#! /usr/bin/python
# -*- coding: utf-8 -*-
import re

import common.readwrite as io
import common.definitions as d


def minsec_to_decimal(infile, outfile):
    """Convert lat/long coordinates from minutes and seconds to decimal."""

    data = io.pull(infile, str)

    out = []
    for coord in data:
        # Splits each coordinate pair into degrees, minutes, seconds, and
        # hemisphere marker.
        coord = coord.upper()
        subs = re.split(r'\s*[°"\',]\s*|.(?=[NESW])|(?<=[NESW]).|\n', coord)
        subs = filter(None, subs)

        names = ['degrees', 'minutes', 'seconds']
        values = dict([(name, 0) for name in names])
        pair = [0, 0]
        for (which, section) in enumerate([subs[:len(subs)/2], subs[len(subs)/2:]]):
            for (i, elem) in enumerate(section):
                if (elem in 'NESW'):
                    sign = -1 if elem in 'SW' else 1
                else:
                    values[names[i % (len(subs)/2)]] = float(elem)
            pair[which] = (values['degrees'] + values['minutes']/60
                           + values['seconds']/3600) * sign
        out.append(pair)

    io.push(interpret_out(out), outfile)

def interpret_out(data):
    out = []
    for line in data:
        out.append('{0:2.7f}, {1:3.7f}'.format(line[0], line[1]))
    return out
