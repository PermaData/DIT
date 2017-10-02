import pytest
import os

from dit_flow.dit_widget.chk_count_valid_records_num import chk_count_valid_records_num

def test_chk_count_valid_records_num(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_num.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_count_valid_records_num('-999.0', log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
#    chk_count_valid_records_num('-999.0', log_file=out_log_file,                       input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Print valid values (not -999.0)\n     Total      Valid    Percent\n        20         16     80.000'
    assert expected_log in actual_log
