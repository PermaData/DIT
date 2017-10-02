import pytest
import os


from dit_flow.dit_widget.replace_txt_remove_right import replace_txt_remove_right

def test_replace_txt_remove_right(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('crapola\nload of crap\ncrap pile')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    replace_txt_remove_right('crap', log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
#    replace_txt_remove_right('crap', log_file=out_log_file,                       output_data_file=out_file,                           input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = 'crap\nload of crap\ncrap'
    expected_log = 'Remove text right of crap\n\n\t Total number =3\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
