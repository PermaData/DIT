import datetime as dt

from dit_flow.dit_widget.common.cast_value import cast_to_datetime, cast_to_integer, cast_to_real, cast_data_value


def test_cast_to_datetime_format1():
    date_str = '2017-10-06 02:15'
    actual = cast_to_datetime(date_str)
    expected = dt.datetime(2017, 10, 6, hour=2, minute=15)
    assert actual == expected


def test_cast_to_datetime_format2():
    date_str = '2017-10-06 02:15:30'
    actual = cast_to_datetime(date_str)
    expected = dt.datetime(2017, 10, 6, hour=2, minute=15, second=30)
    assert actual == expected


def test_cast_to_integer_valid():
    actual = cast_to_integer('3')
    expected = 3
    assert actual == expected


def test_cast_to_real():
    actual = cast_to_real('3.354')
    expected = 3.354
    assert actual == expected


def test_cast_data_value():
    actual = cast_data_value('a_string')
    expected = 'a_string'
    assert actual == expected
