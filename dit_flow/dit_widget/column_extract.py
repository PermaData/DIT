import csv
import os

import rill


@rill.component
@rill.inport('DATAFILE')
@rill.inport('DATAMAP')
@rill.inport('FID')
@rill.inport('SID')
@rill.inport('COLUMNS')
@rill.outport('TEMPIN')
@rill.outport('TEMPOUT')
@rill.outport('DATAFILE_OUT')
@rill.outport('DATAMAP_OUT')
@rill.outport('FID_OUT')
@rill.outport('SID_OUT')
def column_extract(DATAFILE, DATAMAP, FID, SID, COLUMNS, TEMPIN, TEMPOUT,
                   DATAFILE_OUT, DATAMAP_OUT, FID_OUT, SID_OUT):
    """Extracts columns from the input csv file into a temporary file.
    DATAFILE: name of main input csv file
    DATAMAP: dictionary of {column name: column index} within the
    FID: number 1... that identifies the order of the current file
    SID: number 1... that identifies the order of the current step
    COLUMNS: a list of column names to be taken
    """
    for name, map_, step, fileid, columnset in zip(DATAFILE.iter_contents(),
                                                   DATAMAP.iter_contents(),
                                                   SID.iter_contents(),
                                                   FID.iter_contents(),
                                                   COLUMNS.iter_contents()):
        path, base = name.rsplit('/', 1)
        template = '{pth}/{fid}_{sid}_{which}_temp.csv'
        tempin = template.format(pth=path, fid=fileid, sid=step, which='In')
        tempout = template.format(pth=path, fid=fileid, sid=step, which='Out')
        indices = [map_[name] for name in columnset]

        with open(name, newline='') as source, \
             open(tempin, 'w', newline='') as dest:
            data = csv.reader(source, quoting=csv.QUOTE_NONNUMERIC,
                              quotechar="'")
            output = csv.writer(dest, quoting=csv.QUOTE_NONNUMERIC,
                                quotechar="'")
            header = True
            for line in data:
                if (header):
                    header = False
                    continue
                outputline = [line[i] for i in indices]
                output.writerow(outputline)
	
        os.chmod(tempin, 0o666)
        os.chmod(tempout, 0o666)

        TEMPIN.send(tempin)
        TEMPOUT.send(tempout)
        DATAFILE_OUT.send(name)
        DATAMAP_OUT.send(map_)
        FID_OUT.send(fileid)
        SID_OUT.send(step)
