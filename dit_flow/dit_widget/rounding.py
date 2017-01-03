import math

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE_IN')
@rill.inport('MODE')
@rill.inport('PRECISION')
@rill.outport('OUTFILE_OUT')
def rounding(INFILE, OUTFILE_IN, MODE, PRECISION, OUTFILE_OUT):
    """Round values to the nearest integer.

    modes:
        up/ceil/ceiling: round to the next integer towards +inf.
        down/floor: round to the next integer towards -inf.
        trunc/truncate: truncate decimal part, rounding towards 0.
        nearest/round: round to the nearest integer. If precision is
            given, instead round to that many digits beyond the decimal
            point.
    """
    precision_iter = PRECISION.iter_contents()
    for infile, outfile, mode in zip(INFILE.iter_contents(),
                                     OUTFILE_IN.iter_contents(),
                                     MODE.iter_contents()):
        try:
            precision = int(next(precision_iter))
        except StopIteration:
            precision = 0
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)
            output = csv.reader(_out)

            input_map = {'up': _ceil, 'ceil': _ceil, 'ceiling': _ceil,
                         'down': _floor, 'floor': _floor,
                         'trunc': _trunc, 'truncate': _trunc,
                         'nearest': _round, 'round': _round,
                         }
            conv = input_map[mode.lower()]

            for line in data:
                out = []
                for item in line:
                    out.append(conv(item, precision))
                output.writerow(out)

        OUTFILE_OUT.send(outfile)


def _ceil(val, precision):
    if (precision):
        return float(math.ceil(val * 10**precision)) / 10**precision
    else:
        return float(math.ceil(val))


def _floor(val, precision):
    if (precision):
        return float(math.floor(val * 10**precision)) / 10**precision
    else:
        return float(math.floor(val))


def _trunc(val, precision):
    if (precision):
        return int(val * 10**precision) / 10**precision
    else:
        return int(val)


def _round(val, precision):
    return round(val, precision)
