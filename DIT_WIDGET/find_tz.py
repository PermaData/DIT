# -*- coding: utf-8 -*-

from tzwhere import tzwhere
import pytz

import common.readwrite as io

def find_tz(infile, outfile):
    data = io.pull(infile, str)

    finder = tzwhere.tzwhere()
    out = []
    for line in data:
        coord = standardize(line)
        tzname = finder.tzNameAt(*coord)
        out.append(tzname)
        offset = name_to_offset(tzname)

    io.push(out, outfile)

def standardize(coordstring):
    """Creates a tuple from a standard decimal coordinate string."""
    out = coordstring.replace('°','').replace('W','*-1').replace('S','*-1')
    out = out.replace('N','',).replace('E','')
    return eval(out)

def name_to_offset(name):
    # Perhaps use date/time data to process this into UTC times
    # Actually use pytz.timezone(name).localize(datetime object).strftime(necessary values)
    pass
