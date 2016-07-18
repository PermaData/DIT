import csv
import utm
import sys

import common.parseargs as pa

def latlong_to_utm(infile, outfile, lat_i, long_i, header=True):
    with open(infile, 'rb') as original:
        with open(outfile, 'wb') as output:
            data = csv.reader(original)
            push = csv.writer(output)
            for row in data:
                if (header):
                    ENZL = ('East', 'North', 'Zone', '')
                    header = False
                else:
                    lat = float(row[lat_i])
                    long = float(row[long_i])
                    ENZL = utm.from_latlon(lat, long)
                push.writerow(modify_row(row, ENZL, lat_i, long_i))


def modify_row(row, ENZL, lat_i, long_i):
    out = [entry for (i, entry) in enumerate(row) if i not in (lat_i, long_i)]
    modified = ENZL[0:2] + (str(ENZL[2])+ENZL[3],)  # Join the zone number and letter
    out.extend(modified)
    return out


#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
lat_i = args[2][0]
long_i = args[2][1]

latlong_to_utm(infile, outfile, lat_i, long_i)