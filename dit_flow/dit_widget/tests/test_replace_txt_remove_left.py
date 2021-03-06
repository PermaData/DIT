import os
import pytest

from dit_flow.dit_widget.replace_txt_remove_left import replace_txt_remove_left


@pytest.mark.skip()
def test_replace_txt_remove_left(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('crapola\nload of crap\ncrap pile')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    replace_txt_remove_left('crap', True, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file='{}'.format(temp_in_file.strpath))
#    replace_txt_remove_left('crap', True, log_file=out_log_file,                       output_data_file=out_file,                           input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = 'crapola\ncrap\ncrap pile'
    expected_log = 'Remove text left of crap\n'\
        'Record            Old Value            New Value\n'\
        ' 1              crapola              crapola\n'\
        ' 2         load of crap                 crap\n'\
        ' 3            crap pile            crap pile\n'\
        '\n\t Total number =3\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
