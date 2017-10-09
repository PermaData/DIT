import pytest

from dit_flow.dit_widget.rounding import rounding


def test_round_down(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.000\n2.13\n-999.99\n4.55555555\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    rounding('up', precision=2, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    expected_out = "1.0\n2.13\n-999.99\n4.56"
    assert expected_out in actual_out
