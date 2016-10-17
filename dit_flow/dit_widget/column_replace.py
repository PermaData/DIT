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
        print('replace', fid, sid)
        indices = {tempmap[name]: destmap[name] for name in tempmap}
        indices_in = {tempmap[name]: datamap[name] for name in tempmap}

        with open(tempfile, newline='') as _temp, \
             open('tempout', 'w', newline='') as _out, \
             open(destfile, newline='') as _dest, \
             open('tempin', 'w', newline='') as _in, \
             open(datafile, newline='') as _original:
            #  Modifies both the in and out files at the same time
            # BUG: it will fail when trying to write to a renamed column in the input file

            # new = csv.reader(_in, quoting=csv.QUOTE_NONNUMERIC, quotechar="'")
            # existing = csv.reader(_dest, quoting=csv.QUOTE_NONNUMERIC,
            #                       quotechar="'")
            # modified = csv.writer(_out, quoting=csv.QUOTE_NONNUMERIC,
            #                       quotechar="'")
            new = csv.reader(_temp)
            existing = csv.reader(_dest)
            modified_out = csv.writer(_out)
            original = csv.reader(_original)
            modified_in = csv.writer(_in)

            modified_out.writerow(next(existing))
            modified_in.writerow(next(original))
            for nline, eline, oline in zip(new, existing, original):
                output_out = eline
                output_in = oline
                for from_, to_ in indices.items():
                    output_out[to_] = nline[from_]
                for from_, to_ in indices_in.items():
                    output_in[to_] = nline[from_]
                modified_out.writerow(output_out)
                modified_in.writerow(output_in)
        shutil.move('tempout', destfile)
        shutil.move('tempin', datafile)

        print('data out', datafile)
        DATAFILE_OUT.send(datafile)
        print('data map out', datamap)
        DATAMAP_OUT.send(datamap)
        print('fid', fid)
        FID_OUT.send(fid)
        print('sid', sid)
        SID_OUT.send(sid + 1)
        print('dest', destfile)
        DESTFILE_OUT.send(destfile)
        print('dest map', destmap)
        DESTMAP_OUT.send(destmap)
