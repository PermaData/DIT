import pytest
import os

from dit_flow.dit_widget.calc_copy_col import calc_copy_col


def test_calc_copy_col(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n2.0\n-999.99\n4.0\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    calc_copy_col(input_data_file=temp_in_file.strpath, output_data_file=temp_out_file.strpath, log_file=temp_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1.0\n2.0\n-999.99\n4.0\n'
    expected_log = 'Copy input column to output column\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
