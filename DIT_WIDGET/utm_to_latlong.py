#! /usr/bin/python

# Convert UTM to lat/long

# UTM is specified as
# {longitude band number}
# {meters east of the meridian of the longitude band + 500 000}
# {meters north of the equator + 0 if north else 10 000 000}

import csv
import math


def utm_to_latlong(infile, outfile, zone_i, E_i, N_i):
    #zone_i is the 'zone' data column
    # E_i is the 'easting' data column
    # N_i is the 'northing' data column
    
    out = []
    with open(infile, 'r') as f:
        data = csv.reader(f)
        for row in data:
            zone = int(row[zone_i])
            east = float(row[E_i])
            north = float(row[N_i])
            
            
def east_to_longitude(easting, latitude):
    # Assume equatorial radius of Earth is 6378.137 km
    
def north_to_latitude(northing):
    # Assume polar radius of Earth is 6356.752 km
    # 90 degrees = pi/2 * polar radius