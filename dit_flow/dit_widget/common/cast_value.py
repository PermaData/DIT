import datetime as dt

from decimal import Decimal, InvalidOperation

gtnp_date_time_format1 = '%Y-%m-%d %H:%M'
gtnp_date_time_format2 = '%Y-%m-%d %H:%M:%S'
gtnp_date_time_format = gtnp_date_time_format1


def cast_to_datetime(dt_str, logger=None):
    """
    Convert string to a datetime object.
    :param int_str: string to convert to a datetime object
    :return: datetime object
    """
    date_time = None
    dt_str = dt_str.strip()
    try:
        gtnp_date_time_format = gtnp_date_time_format1
        date_time = dt.datetime.strptime(dt_str, gtnp_date_time_format)
    except ValueError as error:
        try:
            gtnp_date_time_format = gtnp_date_time_format2
            date_time = dt.datetime.strptime(dt_str, gtnp_date_time_format)
        except ValueError as error:
            logger.error('"', error, '"')
            logger.error('Column cannot be converted to date/time. Sorting will be by string.')
    return date_time


def cast_to_integer(int_str):
    """
    Convert string to an integer.
    :param int_str: string to convert to an integer
    :return: integer number
    """
    try:
        return int(float(int_str))
    except ValueError:
        return int_str


def cast_float_to_decimal(floatish):
    if isinstance(floatish, str):
        decimal_val = cast_to_decimal(floatish)
    else:
        decimal_val = cast_number_to_decimal(floatish)
    return decimal_val


def cast_number_to_decimal(float_val):
    dec_val = Decimal(str(float_val))
    return dec_val


def cast_to_decimal(decimal_str):
    """
    Convert string to a decimal.
    :param real_str: string to convert to a decimal
    :return: decimal object
    """
    try:
        return Decimal(decimal_str)
    except InvalidOperation:
        return decimal_str


def cast_to_real(real_str):
    """
    Convert string to a real.
    :param real_str: string to convert to a real
    :return: real number
    """
    try:
        return float(Decimal(real_str))
    except ValueError:
        return real_str


def cast_data_value(col_str):
    """
    Cast strings to integers or reals before writing them to the file to avoid
    quoting numerics.
    :param col_str: data string value to possible cast
    :return: an integer, real, or string
    """
    try:
        return int(col_str)
    except ValueError:
        pass
    try:
        return cast_to_real(col_str)
    except (ValueError, InvalidOperation):
        pass
    return col_str
