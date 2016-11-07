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
                    lon = float(row[1])
                    ENZL = utm.from_latlon(lat, lon)
                    ENZL = ENZL[0:2] + (str(ENZL[2])+ENZL[3],)
                output.writerow(ENZL)
        OUTFILE_OUT.send(outfile)
