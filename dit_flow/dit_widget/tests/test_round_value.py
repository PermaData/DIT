from dit_flow.dit_widget.common.round_value import _ceil, _floor, _trunc, _round


def test__ceil():
    float_val = 3.1415
    actual = _ceil(float_val, 3)
    expected = 3.142
    assert actual == expected


def test__floor():
    float_val = 3.1415
    actual = _floor(float_val, 3)
    expected = 3.141
    assert actual == expected


def test__trunc():
    float_val = 3.1415
    actual = _trunc(float_val, 2)
    expected = 3.14
    assert actual == expected


def test__round():
    float_val = 3.14159
    actual = _round(float_val, 3)
    expected = 3.142
    assert actual == expected

    actual = _round(float_val, 2)
    expected = 3.14
    assert actual == expected
