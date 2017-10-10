import pytest

from dit_flow.dit_widget.replace_num_out_range import replace_num_out_range

def test_replace_num_out_range(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n2.0\n-999.99\n4.0\n5.0\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    replace_num_out_range(2.0, 4.0, -999.99, True, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '-999.99\n2.00\n-999.99\n4.00\n-999.99\n'
    expected_log = 'Replacing values < 2.0 or > 4.0 with -999.99\n    Record            Old Value            New Value\n         1                  1.0              -999.99\n         3              -999.99              -999.99\n         5                  5.0              -999.99\n\n\t Total number =3\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
