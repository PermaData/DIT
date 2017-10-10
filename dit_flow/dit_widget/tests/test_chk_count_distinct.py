import pytest
import os

from dit_flow.dit_widget.chk_count_distinct import chk_count_distinct

def test_chk_count_distinct(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_txt.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_count_distinct(log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
#    chk_count_distinct(log_file=out_log_file,                       input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Count distinct values\n'\
'\tTotal number =20\n'\
'  Num                           Distinct Value     number    Percent\n'\
'    1                                     Crap          7     35.000\n'\
'    2                                  Garbage          6     30.000\n'\
'    3                                     junk          4     20.000\n'\
'    4                                       na          3     15.000\n'
    assert expected_log in actual_log
