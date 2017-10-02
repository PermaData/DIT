import pytest

from dit_flow.dit_widget.math_absolute_value import math_absolute_value

def test_absolute_value(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n-2.0\n-999.99\n2.0\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    math_absolute_value(-999.99, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1.00\n2.00\n-999.99\n2.00'
    expected_log = 'Absolute value of column'
    assert expected_out in actual_out
    assert expected_log in actual_log
