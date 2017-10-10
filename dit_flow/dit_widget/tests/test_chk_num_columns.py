import pytest
import os

from dit_flow.dit_widget.chk_num_columns import chk_num_columns

def test_chk_num_columns(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_numcol.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_num_columns(True,log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
#    chk_num_columns(True,log_file=out_log_file,                       output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_log = 'Checking the number of columns\n'\
'	Correct number of columns:          3\n'\
'    Record          Num Columns\n'\
'         3                    4 \n'\
'         4                    4 \n'\
'         7                    2 \n'\
'         8                    2 \n'\
'	Total number rows with incorrect number columns=4\n'
    assert expected_log in actual_log
