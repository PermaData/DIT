import math


def _ceil(val, precision):
    if (precision):
        return float(math.ceil(val * 10 ** precision)) / 10 ** precision
    else:
        return float(math.ceil(val))


def _floor(val, precision):
    if (precision):
        return float(math.floor(val * 10 ** precision)) / 10 ** precision
    else:
        return float(math.floor(val))


def _trunc(val, precision):
    if (precision):
        return int(val * 10 ** precision) / 10 ** precision
    else:
        return int(val)


def _round(val, precision):
    return round(val, precision)
