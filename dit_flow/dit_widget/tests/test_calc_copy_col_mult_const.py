import os

from dit_flow.dit_widget.calc_copy_col_mult_const import calc_copy_col_mult_const


def test_calc_copy_col_mult_const(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_calc.in')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    calc_copy_col_mult_const(10., -999., input_data_file=in_data_file, output_data_file=temp_out_file.strpath, log_file=temp_log_file)
    calc_copy_col_mult_const(10., -999., input_data_file=in_data_file, output_data_file=out_file,              log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '10.00000000,10.00000000\n'\
                   '20.00000000,-999.00000000\n'\
                   '-999.00000000,30.00000000\n'\
                   '-999.00000000,-999.00000000\n'\
                   '50.00000000,0.00000000\n'
    expected_log = 'Copy column and multiply by constant (out = in * constant)\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
