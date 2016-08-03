from setups import *
from helpers import *


@with_setup(setup_numeric)
def test_add_const(infile, outfile, constant=2):
    call_real_function(test_add_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            # This may fail due to precision errors
            assert (almost_equal(float(lineout), float(linein) + constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_div_const(infile, outfile, constant=2):
    call_real_function(test_div_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            # This may fail due to precision errors
            assert (almost_equal(float(lineout), float(linein) / constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_mult_const(infile, outfile, constant=2):
    call_real_function(test_mult_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            # This may fail due to precision errors
            assert (almost_equal(float(lineout), float(linein) * constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_sub_const(infile, outfile, constant=2):
    call_real_function(test_sub_const, infile, outfile, constant)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            # This may fail due to precision errors
            assert (almost_equal(float(lineout), float(linein) - constant) or
                    almost_equal(float(lineout), MISSING))


@with_setup(setup_numeric)
def test_replace_eq(infile, outfile, threshold=777.2, value=MISSING):
    call_real_function(test_replace_eq, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (almost_equal(float(linein), threshold)):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_ge(infile, outfile, threshold=5.233, value=MISSING):
    call_real_function(test_replace_ge, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (almost_equal(float(linein), threshold) or
                float(linein) > threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_gt(infile, outfile, threshold=5.233, value=MISSING):
    call_real_function(test_replace_gt, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (float(linein) > threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_le(infile, outfile, threshold=4.122288, value=MISSING):
    call_real_function(test_replace_le, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (almost_equal(float(linein), threshold) or
                float(linein) < threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_lt(infile, outfile, threshold=4.122288, value=MISSING):
    call_real_function(test_replace_lt, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (float(linein) < threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))


@with_setup(setup_numeric)
def test_replace_notin_rangex(infile, outfile, threshold=(0, 5), value=MISSING):
    call_real_function(test_replace_lt, infile, outfile, threshold, value)

    with open(infile) as IN, open(outfile) as OUT:
        for (linein, lineout) in zip(IN, OUT):
            print linein, lineout
            if (float(linein) < threshold):
                assert almost_equal(float(lineout), value)
            else:
                assert almost_equal(float(linein), float(lineout))