import csv
import itertools


def shard(datafile, header=True, name_override=None):
    """
    Inputs:
        datafile:
        header: If True (the default), the first line of the file is a
            header. If False, there is only data in the file.
        name_override: If None (the default)
    Outputs:
        Writes each column of the data to a different file. The names of
        these files will be either the column headers (if they exist) or
        their zero-indexed position in the file.

        Station,Date,Temperature
        XXX123,1999-03-21,-4.30265

        will produce a file named Station.column containing 'XXX123',
        a file Date.column containing '1999-03-21'.... If there was not
        a header, the files would instead be called 0.column, 1.column,
        and 2.column.
    """
    with open(datafile, 'rb') as f:
        data = csv.reader(f)
        column_check(data)

        # Determine filenames
        firstline = data.readline()
        if (name_override is not None):
            # Use the names given instead of finding them
            # If there are too few
            name = ['' for all in firstline]
            for i in range(len(firstline)):
                if (i < len(name_override) and name_override[i]):
                    # If there is a name given for this position...
                    name[i] = name_override[i]
                else:
                    if (header):
                        name[i] = firstline[i]
                    else:
                        name[i] = i
        elif (header):
            # Use the values found in the header as column file names
            name = firstline
        else:
            # Use column indices as names
            name = list(range(len(firstline)))
            f.seek(0)  # Return to the top of the file to read again

        # Open files
        files = [open(str(item) + '.column', 'w') for item in name]

        # Write columns to files
        try:
        for line in data:
            for (i, item) in enumerate(line):
                files[i].write(str(item))
        except ValueError:
            close_all(files)

        # Close files before exiting
        close_all(files)


def column_check(data):
    # TODO: Check if this exhausts the iterator in containing scope
    """Expects a csv.reader object."""
    count = []
    for line in data:
        count.append(len(line))
    mean = round(float(sum(count)) / len(count))
    error = False
    for (i, item) in enumerate(count):
        if (item != mean):
            print 'Line {0} has a different number of columns than the rest '\
                'of the file.'.format(i+1)
            error = True
    if (error):
        raise IndexError('One or more of the lines was flawed.')
    else:
        return True


def close_all(files):
    for opened in files:
        opened.close()




def reunite(outfile, *args):
    """Unites all column files into a single csv.
    Inputs:
        outfile: The name of the csv file to write into.
        *args: Any number of filenames which hold individual columns. 
            The columns will be put into the output file in the order
            they appear in this function call.
    Outputs:
        Writes into outfile.
    """
    with open(outfile, 'wb') as f:
        final = csv.writer(f)
        files = args[:]
        for (i, name) in enumerate(args):
            files[i] = open(args[i])
            
        for line in itertools.izip(*files):
            final.writerow(line)
            
        close_all(files)