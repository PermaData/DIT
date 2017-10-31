import os

from dit_flow.dit_widget.cond_if_greater_equal import cond_if_greater_equal


def test_cond_if_greater_equal(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_cond.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    out_data_file = os.path.join(this_dir, 'test_calc_out')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    cond_if_greater_equal(5, 'test', True, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
#    cond_if_greater_equal(5, 'test', True, log_file=out_log_file,                       output_data_file=out_data_file,                      input_data_file=in_data_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1,Junk\n2,Junk\n3,Junk\n4,Junk\n5,test\n6,test\n1,Junk\n'\
                   '2,Junk\n3,Junk\n4,Junk\n5,test\n6,test\n'
    expected_log = 'If column A >= 5 set column B = test\n'\
                   '    Record         Col A Value     Old Col B Value     New Col B Value\n'\
                   '         5                   5                Junk                test\n'\
                   '         6                   6                Junk                test\n'\
                   '        11                   5                Junk                test\n'\
                   '        12                   6                Junk                test\n'\
                   '	 Total number =4\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
