import csv
import os

from circuits import Component
from dit_flow.dit_widget.flow_widget import FlowWidget
from dit_flow.dit_widget.port import PortType

class ColumnExtract(Component, FlowWidget):

    channel = 'column_extract'

    name = 'ColumnExtract' # component name in format that can be used in graphs
    description = 'Adds constant to all values in infile and writes the result' \
            ' to outfile',
    input_args = [ # list of input ports
        ('datafile', PortType.STR),
        ('datamap', PortType.STR),
        ('flow_id', PortType.INT),
        ('step_id', PortType.INT),
        ('columns', PortType.STR),
        ('logfile', PortType.STR)
    ]
    outputs_args = [ # list of output ports
        ('tempin', PortType.STR),
        ('tempout', PortType.STR),
        ('datafile_out', PortType.STR),
        ('datamap_out', PortType.STR),
        ('flow_id_out', PortType.INT),
        ('step_id_out', PortType.INT),
        ('logfile_out', PortType.STR)
    ]

    def go(self, *args, **kwargs):
        print("Received args: ", args, kwargs)
        result = column_extract(*args)
        print('result: ', result)
        return result

def column_extract(datafile, datamap, step_id, file_id, columns, logfile, tempin,
                   tempout, datafile_out, datamapout, fid_out, sid_out,
                   logfile_out):
    """Extracts columns from the input csv file into a temporary file.
    DATAFILE: datafile of main input csv file
    DATAMAP: dictionary of {column datafile: column index} within the
    FID: number 1... that identifies the order of the current file
    SID: number 1... that identifies the order of the current step_id
    COLUMNS: a list of column datafiles to be taken
    """
    for datafile, datamap, step_id, file_id, columns, logfile in \
        zip(DATAFILE.iter_contents(), DATAMAP.iter_contents(),
            SID.iter_contents(), FID.iter_contents(),
            COLUMNS.iter_contents(), LOGFILE.iter_contents()):
        # TODO: Log any errors to the log file
        path, base = datafile.rsplit('/', 1)
        template = '{pth}/{fid}_{sid}_{which}_temp.csv'
        tempin = template.format(pth=path, fid=file_id, sid=step_id, which='In')
        tempout = template.format(pth=path, fid=file_id, sid=step_id, which='Out')
        indices = [datamap[datafile] for column in columns]

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

        result = [
            tempin,
            tempout,
            datafile,
            datamap,
            file_id,
            step_id,
            logfile
        ]
        return result
