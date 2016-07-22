# -*- coding: utf-8 -*-
import sys
import datetime
import csv
import getopt

from tzwhere import tzwhere
import pytz

import common.readwrite as io

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
                    dt = datetime.strptime('%Y-%m-%d %H:%M', data[dt_i])
                    offset = name_to_offset(tzname, dt)

                    push.writerow(line + [offset])

    #io.push(out, outfile)

# def standardize(coordstring):
    # """Creates a tuple from a standard decimal coordinate string."""
    # out = coordstring.replace('°','').replace('W','*-1').replace('S','*-1')
    # out = out.replace('N','',).replace('E','')
    # return eval(out)

def name_to_offset(name, dt):
    # Perhaps use date/time data to process this into UTC times
    # Actually use pytz.timezone(name).localize(datetime object).strftime(necessary values)
    tz = pytz.timezone(name)
    actual = tz.localize(dt)
    offset = actual.strftime('%z')
    return int(offset) * 36 / 60 / 60   # Returns offset in possibly fractional hours


def parse_args(args):
    def help():
        print 'find_tz.py -i <input file> -o <output file> -d <date column index> -t <latitude column index> -n <longitude column index>'


    infile = None
    outfile = None
    constant = None
    dt_i = None
    lat_i = None
    lon_i = None

    options = ('i:o:d:t:n:',
               ['input', 'output', 'date_column_index', 'latitude_column_index', 'longitude_column_index'])
    readoptions = zip(['-'+c for c in options[0] if c != ':'],
                      ['--'+o for o in options[1]])

    try:
        (vals, extras) = getopt.getopt(args, *options)
    except getopt.GetoptError as e:
        print str(e)
        help()
        sys.exit(2)

    for (option, value) in vals:
        if (option in readoptions[0]):
            infile = value
        elif (option in readoptions[1]):
            outfile = value
        elif (option in readoptions[2]):
            dt_i = int(value)
        elif (option in readoptions[2]):
            lat_i = int(value)
        elif (option in readoptions[2]):
            lon_i = int(value)

    if (any(val is None for val in [infile, outfile, dt_i, lat_i, lon_i])):
        help()
        sys.exit(2)

    return infile, outfile, dt_i, lat_i, lon_i

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])


find_tz(*args)