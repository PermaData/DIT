#! /usr/bin/python

import csv
import utm
import string
import sys

import common.parseargs as pa


def utm_to_latlong(infile, outfile, zone_i, E_i, N_i, hemisphere='', header=True):
    """Convert values in a csv file from UTM coordinates to latitude/longitude.
    Inputs:
        infile: Name of CSV file that holds the UTM data.
        outfile: Name of CSV file to write recalculated data to
        zone_i: column index in infile with the zone data
        E_i:
        N_i:
        hemisphere:
    Output:
        Writes
    """

    with open(infile, 'rb') as original:
        with open(outfile, 'wb') as output:
            data = csv.reader(original)
            push = csv.writer(output)
            for row in data:
                if (header):
                    latlong = ('Lat', 'Lon')
                    header = False
                else:
                    if (row[zone_i][-1] in string.letters):
                        zoneletter = row[zone_i][-1]
                        zone = int(row[zone_i][:-1])
                        northern = None
                    else:
                        zone = int(row[zone_i])
                        northern = hemisphere.lower() in \
                                   ('n', 'north', 'northern')
                        zoneletter = None
                    east = float(row[E_i])
                    north = float(row[N_i])


                    latlong = utm.to_latlon(east, north, zone,
                                    northern=northern, zone_letter=zoneletter)

                push.writerow(modify_row(row, latlong, zone_i, E_i, N_i))


def modify_row(row, latlong, zone_i, E_i, N_i):
    out = [entry for i, entry in enumerate(row) if i not in (zone_i, E_i, N_i)]
    out.extend(latlong)
    return out

    
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
zone_i = args[2][0]
E_i = args[2][1]
N_i = args[2][2]
hemisphere = args[3][0]

utm_to_latlong(infile, outfile, zone_i, E_i, N_i, hemisphere)