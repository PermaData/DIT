#! /usr/bin/python

# Convert UTM to lat/long

# UTM is specified as
# {longitude band number}
# {meters east of the meridian of the longitude band + 500 000}
# {meters north of the equator + 0 if north else 10 000 000}

import csv
import utm


def utm_to_latlong(infile, outfile, zone_i, E_i, N_i, hemisphere):
    #zone_i is the index of the 'zone' data column
    # E_i is the index of the 'easting' data column
    # N_i is the index of the 'northing' data column

    with open(infile, 'rb') as original:
        with open(outfile, 'wb') as output:
            data = csv.reader(original)
            push = csv.writer(output)
            header = True
            for row in data:
                if (header):
                    header = False
                    continue
                zone = int(row[zone_i])
                east = float(row[E_i])
                north = float(row[N_i])

                push.writerow(
                    utm.to_latlon(east, north, zone, northern=(
                        hemisphere.lower() in ['n', 'north', 'northern'])))
