import pytest
import os

from dit_flow.dit_widget.chk_count_valid_records_txt import chk_count_valid_records_txt

def test_chk_count_valid_records_txt(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_txt.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_count_valid_records_txt('na', log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
#    chk_count_valid_records_txt('na', log_file=out_log_file,                       input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Print valid values (not na)\n     Total      Valid    Percent\n        20         17     85.000'
    assert expected_log in actual_log
