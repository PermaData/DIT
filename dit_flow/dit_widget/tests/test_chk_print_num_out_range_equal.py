import pytest
import os

from dit_flow.dit_widget.chk_print_num_out_range_equal import chk_print_num_out_range_equal

def test_chk_print_num_out_range_equal(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_print.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
#    chk_print_num_out_range_equal(-8.0, 9.0, log_file=out_log_file, input_data_file=in_data_file)
    chk_print_num_out_range_equal(-8.0, 9.0, log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Print values <= -8.0 or >= 9.0\n    Record                Value\n         1                 -9.0\n         2                -8.00\n        19                  9.0\n        20                10.00\n\n	 Total number <= -8.0 or >= 9.0:          4\n'
    assert expected_log in actual_log
