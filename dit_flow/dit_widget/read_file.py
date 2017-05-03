import csv
import os

from circuits import Component

class ReadFile(Component):

    channel = 'ReadFile'

    def go(self, event):
        print(self.channel, ' received go event')

# IMPORTANT: the order of the decorators has to correspond to the order of the arguments
def read_file(FILENAME, FID, LOGFILE, DESTFILE, FID_OUT, LOGFILE_OUT):
    for name, ID, logfile in zip(FILENAME.iter_contents(), FID.iter_contents(),
                                 LOGFILE.iter_contents()):
        path, base = name.rsplit('/', 1)
        main_name = '{pth}/{ID}_In_{base}.csv'.format(pth=path, ID=ID,
                                                      base=base)
        with open(name, newline='') as _from, \
             open(main_name, 'w', 0o666, newline='') as _to:
            data = csv.reader(_from, quoting=csv.QUOTE_NONNUMERIC,
                              quotechar="'")
            try:
                isOK = column_check(data)
            except IOError as e:
                with open(logfile, 'a') as log:
                    print(e, file=log)
                isOK = False
            _from.seek(0)
            output = csv.writer(_to, quoting=csv.QUOTE_NONNUMERIC,
                                quotechar="'")
            # Copies the data into the file that will be base input from now on
            for line in data:
                output.writerow(line)

        if (isOK):
            DESTFILE.send(main_name)
            FID_OUT.send(ID)
            LOGFILE_OUT.send(logfile)


def column_check(data):
    # TODO: Check if this exhausts the iterator in containing scope
    # NOTE: It does, you need to reset with a seek(0) command
    # TODO: Pass in the log file so errors can be saved for later inspection
    """Expects a csv.reader object."""
    count = []
    for line in data:
        count.append(len(line))
    mean = round(float(sum(count)) / len(count))
    error = False
    for (i, item) in enumerate(count):
        if (item != mean):
            print('Line {0} has a different number of columns than the rest '
                  'of the file.'.format(i + 1))
            error = True
    if (error):
        raise IOError('One or more of the lines was flawed.')
    else:
        return True
