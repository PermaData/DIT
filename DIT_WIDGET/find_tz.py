# -*- coding: utf-8 -*-
import sys
import datetime as dt
import csv

from tzwhere import tzwhere
import pytz

import common.readwrite as io
import common.parseargs as pa

def find_tz(infile, outfile, dt_i, lat_i, lon_i, header=True):
    """Needs lat and lon in decimal format and needs date/time in GTN-P standard."""
    #data = io.pull(infile, str)

    with open(infile) as input:
        with open(outfile) as output:
            data = csv.reader(input)
            push = csv.writer(output)

            finder = tzwhere.tzwhere()
            out = []
            for line in data:
                if (header):
                    push.writerow(line+['UTC Offset'])
                    header = False
                else:
                    coord = (float(data[lat_i]), float(data[lon_i]))
                    tzname = finder.tzNameAt(*coord)
                    out.append(tzname)
                    datetime = dt.strptime('%Y-%m-%d %H:%M', data[dt_i])
                    offset = name_to_offset(tzname, datetime)
                    
                    push.writerow(line + [offset])

    #io.push(out, outfile)

# def standardize(coordstring):
    # """Creates a tuple from a standard decimal coordinate string."""
    # out = coordstring.replace('°','').replace('W','*-1').replace('S','*-1')
    # out = out.replace('N','',).replace('E','')
    # return eval(out)

def name_to_offset(name, datetime):
    # Perhaps use date/time data to process this into UTC times
    # Actually use pytz.timezone(name).localize(datetime object).strftime(necessary values)
    tz = pytz.timezone(name)
    actual = tz.localize(datetime)
    offset = actual.strftime('%z')
    return int(offset) * 36 / 60 / 60   # Returns offset in possibly fractional hours


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
dt_i = args[2][0]
lat_i = args[2][1]
lon_i = args[2][2]

find_tz(infile, outfile, dt_i, lat_i, lon_i)