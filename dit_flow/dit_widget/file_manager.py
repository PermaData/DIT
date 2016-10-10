from ..rill import rill


@rill.component
@rill.inport('FILENAMES')
@rill.outport('CURRENT')
@rill.outport('FID')
def file_manager(FILENAMES, CURRENT, FID):
    """
    takes in a collection of file names through that port
    does some preprocessing? at least verify that the file exists
    perhaps copy the original file into a temporary one?
    sends the CURRENT file that needs to be processed to the other port
    """
    """
    for name in FILENAMES:
        try:
            f = open(name)
            CURRENT.send(name)
        except FileNotFoundError:
            drop severity to a warning and don't pass the file on
    """
    for fileset in FILENAMES.iter_contents():
        for name in fileset:
            identifier = 1
            try:
                f = open(name)
                f.close()
                CURRENT.send(name)
                FID.send(identifier)
                identifier += 1
            except FileNotFoundError:
                # TODO: Make this send to some log instead of the console
                print('The file {f} was not found.'.format(f=name))
