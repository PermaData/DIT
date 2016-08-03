import os

from context import *

MISSING = -999.


def with_file(filename):
    """This decorator takes care of passing the infile and outfile
    arguments to any function.
    """

    def decorator(func):
        def decorated(*args):
            infile = filename
            outfile = filename.split('.', 1)[0] + '_' + func.__name__ + '.out'
            
            print 'calling', func.__name__, infile, outfile

            rv = func(infile, outfile, *args)

            # os.remove('.\\' + infile)
            # os.remove('.\\' + outfile)

            return rv

        decorated.__name__ = func.__name__
        return decorated

    return decorator


def call_real_function(testfunction, *args):
    # Relies on test function name being test_<real function>
    name = testfunction.__name__.split('_', 1)[1]
    # Relies on function name being same as module name
    realfunc = getattr(globals()[name], name)
    return realfunc(*args)


def almost_equal(float1, float2):
    return abs(float1 - float2) < 0.0000001


print globals()