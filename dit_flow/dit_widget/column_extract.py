import csv
import os

from circuits import Component

class ColumnExtract(Component):

    channel = 'ColumnExtract'

    def go(self, event):
        print(self.channel, ' received go event')

def column_extract(datafile, datamap, step_id, file_id, columnset, logfile, tempin,
                   tempout, datafile_out, datamapout, fid_out, sid_out,
                   logfile_out):
    """Extracts columns from the input csv file into a temporary file.
    DATAFILE: datafile of main input csv file
    DATAMAP: dictionary of {column datafile: column index} within the
    FID: number 1... that identifies the order of the current file
    SID: number 1... that identifies the order of the current step_id
    COLUMNS: a list of column datafiles to be taken
    """
    for datafile, datamap, step_id, file_id, columnset, logfile in \
        zip(DATAFILE.iter_contents(), DATAMAP.iter_contents(),
            SID.iter_contents(), FID.iter_contents(),
            COLUMNS.iter_contents(), LOGFILE.iter_contents()):
        # TODO: Log any errors to the log file
        path, base = datafile.rsplit('/', 1)
        template = '{pth}/{fid}_{sid}_{which}_temp.csv'
        tempin = template.format(pth=path, fid=file_id, sid=step_id, which='In')
        tempout = template.format(pth=path, fid=file_id, sid=step_id, which='Out')
        indices = [datamap[datafile] for column in columnset]

        with open(datafile, newline='') as source, \
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

        # Create tempout as an empty file so we can set permissions here as opposed to in the widget
        open(tempout, 'a').close()
        os.chmod(tempin, 0o666)
        os.chmod(tempout, 0o666)

        TEMPIN.send(tempin)
        TEMPOUT.send(tempout)
        DATAFILE_OUT.send(datafile)
        DATAdatamapOUT.send(datamap)
        FID_OUT.send(file_id)
        SID_OUT.send(step_id)
        LOGFILE_OUT.send(logfile)
