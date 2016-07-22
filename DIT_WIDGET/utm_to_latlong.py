#! /usr/bin/python

import csv
import utm
import string
import sys
import getopt
import optparse


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


# def parse_args(args):
    # infile = None
    # outfile = None
    # zone_col = None
    # east_col = None
    # north_col = None

    # hemisphere = 'north'

    # p = optparse.OptionParser()
    # p.add_option('-i', '--input', dest='infile', help='input CSV file')
    # p.add_option('-o', '--output', dest='outfile', help='output CSV file')
    # p.add_option('-z', '--zone_index', dest='zone_col', help='zone column index', type='int')
    # p.add_option('-e', '--easting_index', dest='east_col', help='easting column index', type='int')
    # p.add_option('-n', '--northing_index', dest='north_col', help='northing column index', type='int')
    # p.add_option('-H', '--hemisphere', dest='hemisphere', help='hemisphere')

    # map = {'infile': infile, 'outfile': outfile, 'zone_col': zone_col, 'east_col': east_col, 'north_col': north_col, 'hemisphere': hemisphere}

    # (opts, extras) = p.parse_args(args)

    # for name in map:
        # map[name] = getattr(opts, name)

    # if (any(item is None for item in map.items())):
        # # At least one of the values went unset
        # p.print_help()
        # sys.exit(2)

    # return map['infile'], map['outfile'], map['zone_col'], map['east_col'], map['north_col'], map['hemisphere']

def parse_args(args):
    def help():
        print 'utm_to_latlong.py -i <input CSV file> -o <output csv file> -z <zone column index> -e <easting column index> -n <northing column index> [-h <hemisphere>]\nCheck that your argument list is correct.'


    infile = None
    outfile = None
    zone_col = None
    east_col = None
    north_col = None

    hemisphere = 'north'

    options = ('i:o:z:e:n:h:',
                ['input', 'output', 'zone_index', 'easting_index',
                'northing_index', 'hemisphere'])
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
            zone_col = int(value)
        elif (option in readoptions[3]):
            east_col = int(value)
        elif (option in readoptions[4]):
            north_col = int(value)
        elif (option in readoptions[5]):
            hemisphere = value

    if (any(val is None for val in
            [infile, outfile, zone_col, east_col, north_col])):
        help()
        sys.exit(2)

    return infile, outfile, zone_col, east_col, north_col, hemisphere

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = parse_args(sys.argv[1:])
# infile = args[0]
# outfile = args[1]
# zone_i = args[2][0]
# E_i = args[2][1]
# N_i = args[2][2]
# hemisphere = args[3][0]

utm_to_latlong(*args)