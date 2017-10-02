import pytest
import os

from dit_flow.dit_widget.chk_print_num_in_range import chk_print_num_in_range

def test_chk_print_num_in_range(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_print.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
#    chk_print_num_in_range(1.0, 3.0, log_file=out_log_file, input_data_file=in_data_file)
    chk_print_num_in_range(1.0, 3.0, log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Print values > 1.0 and < 3.0\n    Record                Value\n        12                    2\n\n	 Total number > 1.0 and < 3.0:          1'
    assert expected_log in actual_log
