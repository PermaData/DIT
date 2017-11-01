import os

from dit_flow.dit_widget.calc_divide_col import calc_divide_col


def test_calc_divide_col(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_calc.in')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    calc_divide_col(-999., input_data_file=in_data_file, output_data_file=temp_out_file.strpath, log_file=temp_log_file)
#    calc_divide_col(-999., input_data_file=in_data_file, output_data_file=out_file,              log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1.0000000000\n-999.0000000000\n-999.0000000000\n'\
                   '-999.0000000000\n-999.0000000000\n4.2631583214\n'
    expected_log = 'Divide two columns (out = column_a / column_b)\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
