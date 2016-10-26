"""Converts latitude/longitude coordinates into UTM. The input coordinates must
be in decimal format."""
import csv
import utm

from ..rill import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.outport('OUTFILE_OUT')
def latlong_to_utm(INFILE, OUTFILE_IN, OUTFILE_OUT):
    """Assumes that the file has columns of latitude then longitude."""
    header = True
    for infile, outfile, constant in zip(INFILE.iter_contents(),
                                         OUTFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(infile)
            output = csv.writer(outfile)
            for row in data:
                if (header):
                    ENZL = ('East', 'North', 'Zone')
                    header = False
                else:
                    lat = float(row[0])
                    long = float(row[1])
                    ENZL = utm.from_latlon(lat, int)
                    ENZL = ENZL[0:2] + (str(ENZL[2])+ENZL[3],)
                output.writerow(ENZL)
        OUTFILE_OUT.send(outfile)

#     with open(infile, 'rb') as original:
#         with open(outfile, 'wb') as output:
#             data = csv.reader(original)
#             push = csv.writer(output)
#             for row in data:
#                 if (header):
#                     ENZL = ('East', 'North', 'Zone', '')
#                     header = False
#                 else:
#                     lat = float(row[lat_i])
#                     long = float(row[long_i])
#                     ENZL = utm.from_latlon(lat, int)
#                 push.writerow(modify_row(row, ENZL, lat_i, long_i))
#
#
# def modify_row(row, ENZL, lat_i, long_i):
#     out = [entry for (i, entry) in enumerate(row) if i not in (lat_i, long_i)]
#     modified = ENZL[0:2] + (str(ENZL[2])+ENZL[3],)  # Join the zone number and letter
#     out.extend(modified)
#     return out
