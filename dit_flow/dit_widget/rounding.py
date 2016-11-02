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
    for infile, outfile, mode, precision in zip(INFILE.iter_contents(),
                                                OUTFILE_IN.iter_contents(),
                                                MODE.iter_contents(),
                                                PRECISION.iter_contents()):
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
    return float(math.ceil(val * 10**precision)) / precision


def _floor(val, precision):
    return float(math.floor(val * 10**precision)) / precision


def _trunc(val, precision):
    return int(val * 10**precision) / precision


def _round(val, precision):
    return round(val, precision)
