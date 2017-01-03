import os

import rill


@rill.component
@rill.inport('FILENAMES')
@rill.outport('CURRENT')
@rill.outport('FID')
@rill.outport('LOGFILE')
def file_manager(FILENAMES, CURRENT, FID, LOGFILE):
    """
    FILENAMES: a sequence of paths to data files
    CURRENT: sends out a sequence of filenames after confirming they exist
    FID: a sequential numeric identifier for each file
    LOGFILE: sends out a sequence of log filenames that correspond to a data file
    """
    for identifier, name in enumerate(FILENAMES.iter_contents()):
        path, fname = name.rsplit('/', 1)
        log_name = '{pth}/{name}.log'.format(pth=path, name=fname)
        try:
            # Open the file. If the file doesn't exist, the error will be
            # caught.
            f = open(name, 'r')
            f.close()
            # Create/clear the log file
            open(log_name, 'w').close()
            os.chmod(log_name, 0o666)
            CURRENT.send(name)
            FID.send(identifier + 1)
            LOGFILE.send(log_name)
        except FileNotFoundError:
            with open(log_name, 'w') as log:
                print('The file {f} was not found.'.format(f=name), file=log)
