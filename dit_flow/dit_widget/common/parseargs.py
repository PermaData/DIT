#! /usr/bin/python


def parse_args(args):
    """Interpret a list of arguments from the command line.
    Input:
        args: sys.argv[1:]
        This needs to be in the format [-flag value]*
        The allowed flags are:
            i: The following value is the name or path of the input file
            o: The following value is the name or path of the output file
            n: The following value is a numerical argument
            f: the following value is a string argument
    Output:
        (infile, outfile, nums, strs)
        infile is written with the -i flag. It is an error to leave this
            unassigned.
        outfile is written with the -o flag. It is an error to leave
            this unassigned.
        nums is a list of numerical values written by the -n flag.
        strs is a list of strings written by the -f flag.
    """
    # Initialize output variables
    infile = ''
    outfile = ''
    nums = []
    strs = []

    i = 0
    while(i < len(args)):
        if(args[i] == '-i'):
            i += 1
            infile = args[i]
        elif(args[i] == '-o'):
            i += 1
            outfile = args[i]
        elif(args[i] == '-n'):
            i += 1
            nums.append(float(args[i]))
        elif(args[i] == '-f'):
            i += 1
            strs.append(args[i])
        i += 1

    return (infile, outfile, nums, strs)
