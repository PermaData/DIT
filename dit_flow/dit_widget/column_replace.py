import csv
import os
import shutil

from ..rill import rill


@rill.component
@rill.inport('TEMPFILE')
@rill.inport('TEMPMAP')
@rill.inport('DATAFILE')
@rill.inport('DATAMAP')
@rill.inport('FID')
@rill.inport('SID')
@rill.inport('DESTFILE')
@rill.inport('DESTMAP')
@rill.outport('DATAFILE_OUT')
@rill.outport('DATAMAP_OUT')
@rill.outport('FID_OUT')
@rill.outport('SID_OUT')
@rill.outport('DESTFILE_OUT')
@rill.outport('DESTMAP_OUT')
def column_replace(TEMPFILE, TEMPMAP, DATAFILE, DATAMAP, FID, SID, DESTFILE,
                   DESTMAP, DATAFILE_OUT, DATAMAP_OUT, FID_OUT, SID_OUT,
                   DESTFILE_OUT, DESTMAP_OUT):
    # TODO: Add information-writing functionality, like a file to write statistics to
    # The initialization of this file needs to happen in read_file though
    for tempfile, tempmap, datafile, datamap, fid, sid, destfile, destmap in \
        zip(TEMPFILE.iter_contents(), TEMPMAP.iter_contents(),
            DATAFILE.iter_contents(), DATAMAP.iter_contents(),
            FID.iter_contents(), SID.iter_contents(),
            DESTFILE.iter_contents(), DESTMAP.iter_contents()):
        indices = {tempmap[name]: datamap[name] for name in tempmap}

        with open(tempfile, newline='') as _in, \
             open('temp', 'w', newline='') as _out, \
             open(destfile, newline='') as _dest:
            new = csv.reader(_in, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")
            existing = csv.reader(_dest, quoting=csv.QUOTE_NONNUMERIC,
                                  quotechar="'")
            modified = csv.writer(_out, quoting=csv.QUOTE_NONNUMERIC,
                                  quotechar="'")
            for nline, eline in zip(new, existing):
                output = eline
                for from_, to_ in indices.items():
                    output[to_] = nline[from_]
                modified.writerow(output)
        shutil.move('temp', destfile)

        DATAFILE_OUT.send(datafile)
        DATAMAP_OUT.send(datamap)
        FID_OUT.send(fid)
        SID_OUT.send(sid + 1)
        DESTFILE_OUT.send(destfile)
        DESTMAP_OUT.send(destmap)
