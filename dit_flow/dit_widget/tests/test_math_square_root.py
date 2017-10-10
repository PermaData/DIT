import pytest

from dit_flow.dit_widget.math_square_root import math_square_root

def test_math_square_root(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n4.0\n-999.99\n-4.0\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    math_square_root(-999.99, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1.00\n2.00\n-999.99\n-999.99'
    expected_log = 'Square root of values in column'
    assert expected_out in actual_out
    assert expected_log in actual_log
