"""Finds the time zone given latitude and longitude coordinates. If local date
and time are given, account for DST as well."""
import datetime
import time
import csv

from tzwhere import tzwhere
import pytz


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def find_tz(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """
    Inputs:
        infile: name of input csv file.
        outfile: name of output csv file.
    Assumes that the columns are date/time (in GTN-P standard format),
        then latitude (as a signed decimal number, where North is positive),
        then longitude (as a signed decimal number, where East is positive)
    """
    header = True
    for infile, outfile in zip(INFILE.iter_contents(), OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, newline='', 'w') as out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            finder = tzwhere.tzwhere()
            for line in data:
                if (header):
                    output.writerow(line+['UTC Offset'])
                    header = False
                else:
                    coord = (float(line[1]), float(line[2]))
                    tzname = finder.tzNameAt(*coord)
                    tm = time.strptime(line[0].strip(), '%Y-%m-%d %H:%M')
                    dt = datetime.datetime(tm.tm_year, tm.tm_mon, tm.tm_mday,
                                           tm.tm_hour, tm.tm_min)
                    offset = name_to_offset(tzname, dt)

                    output.writerow(line + [offset])


def name_to_offset(name, dt):
    """Uses the pytz library to find the local offset from UTC."""
    tz = pytz.timezone(name)
    actual = tz.localize(dt)
    offset = actual.strftime('%z')
    # Returns offset in possibly fractional hours
    return int(offset) * 36 / 60 / 60
