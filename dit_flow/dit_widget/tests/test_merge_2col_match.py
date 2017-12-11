import pytest
import os

from dit_flow.dit_widget.merge_2col_match import merge_2col_match


@pytest.mark.skip()
def test_merge_2col_match(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    merge_file = os.path.join(this_dir, 'merge_merge_file')
    merge_map = os.path.join(this_dir, 'merge_var_map')
    in_data_file = os.path.join(this_dir, 'merge_in_file')
    out_log_file = os.path.join(this_dir, 'merge_log')
    out_data_file = os.path.join(this_dir, 'merge_out_file')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    merge_2col_match(1, 2, 1, 2, merge_map,merge_file,
                     log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
#    merge_2col_match(1, 2, 1, 2, merge_map,merge_file,
#                     log_file=out_log_file,                       output_data_file=out_data_file,                      input_data_file=in_data_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = 'in_col1,in_col2,in_col3,in_col4,in_col5\n'\
                   '1,a,-999,-999,-999\n'\
                   '1,b,-999,7,7\n'\
                   '2,a,-999,-999,-999\n'\
                   '2,b,-999,7,7\n'\
                   '3,a,-999,-999,-999\n'\
                   '3,b,-999,7,7\n'\
                   '4,a,-999,-999,-999\n'\
                   '4,b,-999,7,7\n'
    expected_log = 'Merge Files\n'\
                   '\tMerge file: /projects/MULTIMOD/PermaData/dit-widget-work/dit_flow.dit_widget/tests/merge_merge_file\n'\
                   '\tMap file: /projects/MULTIMOD/PermaData/dit-widget-work/dit_flow.dit_widget/tests/merge_var_map\n'\
                   '\tRecords merged input file: 4\n'\
                   '\tUnmatched records in merge file: 1\n'\
                   '\t  Rec                           col1                           col2\n'\
                   '\t    5                              5                              c\n'

    assert expected_out in actual_out
    assert expected_log in actual_log
