import pytest
import os


from dit_flow.dit_widget.replace_num_fill import replace_num_fill

def test_replace_num_fill(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('abcdefg\nload of crap\npile')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    replace_num_fill('-999.0', log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
#    replace_num_fill('-999.0', log_file=out_log_file,                       output_data_file=out_file,                           input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '-999.0\n-999.0\n-999.0'
    expected_log = 'Filling with -999.0\n\n\t Total number =3\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
