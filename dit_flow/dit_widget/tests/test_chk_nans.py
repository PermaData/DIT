import os

from dit_flow.dit_widget.chk_nans import chk_nans


def test_chk_nans(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_nans.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n2.0\n-999.99\n4.0\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_nans(True, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
#    chk_nans(True, log_file=out_log_file,                       output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Find values that are not numbers\n'\
                   '    Record               Value\n'\
                   '         4                  na\n'\
                   '        10                  na\n'\
                   '        14                  na\n'\
                   '	Total number =3'
    assert expected_log in actual_log
