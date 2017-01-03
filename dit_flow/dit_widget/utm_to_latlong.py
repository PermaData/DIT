#! /usr/bin/python

import csv
import string

import utm
import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def utm_to_latlong(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """Converts UTM coordinates into latitude/longitude.
    assumes rows are easting, northing, zone number[, optional zone letter]
    if the zone letter is concatenated with the zone number, that also works
    """
    hemisphere = ''
    for infile, outfile in zip(INFILE.iter_contents(),
                               OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for row in data:
                if (length(row) == 4):
                    zoneletter = row[3]
                    northern = None
                elif (row[2][-1] in string.letters):
                    zoneletter = row[2][-1]
                    zone = int(row[2][:-1])
                    northern = None
                else:
                    zone = int(row[2])
                    northern = hemisphere.lower() in ('n', 'north', 'northern')
                    zoneletter = None
                east = float(row[0])
                north = float(row[1])

                latlong = utm.to_latlon(east, north, zone, northern=northern,
                                        zone_letter=zoneletter)
        OUTFILE_OUT.send(outfile)
