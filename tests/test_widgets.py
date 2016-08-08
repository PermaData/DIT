import re
import itertools

from setups import *
from helpers import *

"""

ARITHMETIC OPERATIONS
---------------------

"""


@with_setup(setup_numeric)
def test_add_const(infile, outfile):
    constant = 2
    call_real_function(test_add_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            assert (almost_equal(float(lineout), float(linein) + constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_div_const(infile, outfile):
    constant = 2
    call_real_function(test_div_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            assert (almost_equal(float(lineout), float(linein) / constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_mult_const(infile, outfile):
    constant = 2
    call_real_function(test_mult_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            assert (almost_equal(float(lineout), float(linein) * constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_sub_const(infile, outfile):
    constant = 2
    call_real_function(test_sub_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            assert (almost_equal(float(lineout), float(linein) - constant) or
                    almost_equal(float(lineout), MISSING))


"""

REPLACEMENT OPERATIONS
----------------------

"""


@with_setup(setup_numeric)
def test_replace_eq(infile, outfile):
    threshold = 777.2
    value = MISSING
    call_real_function(test_replace_eq, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (almost_equal(float(linein), threshold)):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_ge(infile, outfile):
    threshold = 5.233
    value = MISSING
    call_real_function(test_replace_ge, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (almost_equal(float(linein), threshold) or
                    float(linein) > threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_gt(infile, outfile):
    threshold = 5.233
    value = MISSING
    call_real_function(test_replace_gt, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (float(linein) > threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_le(infile, outfile):
    threshold = 4.122288
    value = MISSING
    call_real_function(test_replace_le, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (almost_equal(float(linein), threshold) or
                    float(linein) < threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_lt(infile, outfile):
    threshold = 4.122288
    value = MISSING
    call_real_function(test_replace_lt, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (float(linein) < threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_notin_rangex(infile, outfile):
    threshold = (0, 5)
    value = MISSING
    call_real_function(test_replace_notin_rangex, infile, outfile,
                       threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (float(linein) < threshold[0] or float(linein) > threshold[1]):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_rangex(infile, outfile):
    threshold = (0, 5)
    value = MISSING
    call_real_function(test_replace_rangex, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()
        for (linein, lineout) in zip(IN, OUT):
            if (float(linein) > threshold[0] and float(linein) < threshold[1]):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


"""

PRINT OPERATIONS
----------------

"""


@with_setup(setup_numeric)
def test_print_ge(infile, outfile):
    threshold = 5.233
    call_real_function(test_print_ge, infile, outfile, threshold)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()  # Discard number written
        lineout = OUT.next()
        for linein in IN:
            if (almost_equal(float(linein), threshold) or
                    float(linein) > threshold):
                value = re.match('[0-9]+,([\-0-9.]+)', lineout).groups()[0]
                print linein.strip(), value
                assert almost_equal(float(value), float(linein))
                try:
                    lineout = OUT.next()
                except StopIteration:
                    break


@with_setup(setup_numeric)
def test_print_gt(infile, outfile):
    threshold = 5.233
    call_real_function(test_print_gt, infile, outfile, threshold)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()  # Discard number written
        lineout = OUT.next()
        for linein in IN:
            if (float(linein) > threshold):
                value = re.match('[0-9]+,([\-0-9.]+)', lineout).groups()[0]
                assert almost_equal(float(value), float(linein))
                try:
                    lineout = OUT.next()
                except StopIteration:
                    break


@with_setup(setup_numeric)
def test_print_le(infile, outfile):
    threshold = 4.122288
    call_real_function(test_print_le, infile, outfile, threshold)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()  # Discard number written
        lineout = OUT.next()
        for linein in IN:
            if (almost_equal(float(linein), threshold) or
                    float(linein) < threshold):
                value = re.match('[0-9]+,([\-0-9.]+)', lineout).groups()[0]
                assert almost_equal(float(value), float(linein))
                try:
                    lineout = OUT.next()
                except StopIteration:
                    break


@with_setup(setup_numeric)
def test_print_lt(infile, outfile):
    threshold = 4.122288
    call_real_function(test_print_lt, infile, outfile, threshold)

    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()  # Discard number written
        lineout = OUT.next()
        for linein in IN:
            if (float(linein) < threshold):
                value = re.match('[0-9]+,([\-0-9.]+)', lineout).groups()[0]
                assert almost_equal(float(value), float(linein))
                try:
                    lineout = OUT.next()
                except StopIteration:
                    break


"""

STATISTICAL OPERATIONS
----------------------

"""


@with_setup(setup_statistics)
def test_statistics(infile, outfile):
    call_real_function(test_statistics, infile, outfile)

    correct = {'Min': 2,
               'Max': 4,
               'Total points': 6,
               'Valid points': 5,
               'Standard Deviation': 1,
               'Valid fraction': 0.8333333,
               'Mean': 3}

    with open(outfile) as OUT:
        for line in OUT:
            name, valuestr = re.match('([A-Za-z ]+): ([0-9.]+)', line).groups()
            value = float(valuestr)

            assert almost_equal(value, correct[name])


@with_setup(setup_statistics)
def test_pdf(infile, outfile):
    # More difficult because more switches
    bins = (1, 3)
    minmax = ('auto', 'manual')
    lower = (-1, )
    upper = (2, )
    outliers = ('exclude', 'include')
    norm = ('raw', 'probability')

    for args in itertools.product(bins, minmax, lower, upper, outliers, norm):
        bins_ = args[0]
        minmax_ = args[1]
        outliers_ = args[4]
        norm_ = args[5]
        correct = {'Minimum': None, 'Maximum': None, 1: None, 2: None, 3: None}
        if (norm_ == 'raw'):
            if (minmax_ == 'auto'):
                mini = 2
                maxi = 4
                if (bins_ == 3):
                    abc = (2, 1, 2)
                elif (bins_ == 1):
                    abc = (5, )
            elif (minmax_ == 'manual'):
                mini = lower[0]
                maxi = upper[0]
                if (outliers_ == 'exclude'):
                    if (bins_ == 3):
                        abc = (0, 0, 2)
                    elif (bins_ == 1):
                        abc = (2, )
                elif (outliers_ == 'include'):
                    if (bins_ == 3):
                        abc = (0, 0, 5)
                    elif (bins_ == 1):
                        abc = (5, )
        elif (norm_ == 'probability'):
            if (minmax_ == 'auto'):
                mini = 2
                maxi = 4
                if (bins_ == 3):
                    abc = (.4, .2, .4)
                elif (bins_ == 1):
                    abc = (1, )
            elif (minmax_ == 'manual'):
                mini = lower[0]
                maxi = upper[0]
                if (outliers_ == 'exclude'):
                    if (bins_ == 3):
                        abc = (0, 0, 1)
                    elif (bins_ == 1):
                        abc = (1, )
                elif (outliers_ == 'include'):
                    if (bins_ == 3):
                        abc = (0, 0, 1)
                    elif (bins_ == 1):
                        abc = (1, )
        correct.update(dict(zip((1, 2, 3), abc)))
        correct['Maximum'] = maxi
        correct['Minimum'] = mini

        call_real_function(test_pdf, infile, outfile, *args)
        with open(outfile) as OUT:
            for (i, line) in enumerate(OUT):
                print line
                name, valuestr, barevalue = \
                    re.match('(M..imum): ([\-0-9.]+)|([0-9.]+)', line).groups()
                if (name is not None):
                    # Checks min and max
                    assert almost_equal(correct[name], float(valuestr))
                else:
                    # Checks pdf values
                    assert almost_equal(correct[i], float(barevalue))


@with_setup(setup_statistics)
def test_print_max(infile, outfile):
    call_real_function(test_print_max, infile, outfile)
    correct = (())
    with open(infile) as IN, open(outfile) as OUT:
        OUT.next()  # Discard number written
        lineout = OUT.next()
        isMin = True
        for lineout in OUT:
            location, value = lineout.split(',')
            if (location == 'Location'):
                if (value.strip() == 'Maximum'):
                    isMin = False
                continue
            if (isMin):
                assert int(location) in (0, 1)
                assert float(value) == 2
            else:
                assert int(location) in (3, 4)
                assert float(value) == 4


"""

COORDINATE FORMAT CONVERSION

"""


@with_setup(setup_latlong)
def test_minsec_to_decimal(infile, outfile):
    call_real_function(test_minsec_to_decimal, infile, outfile)
    with open(outfile) as OUT:
        for line in OUT:
            values = line.split(',')
            assert almost_equal(float(values[0]), 32.30642, precision=5)
            assert almost_equal(float(values[1]), -122.61458, precision=5)
