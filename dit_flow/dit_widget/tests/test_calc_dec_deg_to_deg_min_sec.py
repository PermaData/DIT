import os

from dit_flow.dit_widget.calc_dec_deg_to_deg_min_sec import calc_dec_deg_to_deg_min_sec


def test_calc_dec_deg_to_deg_min_sec(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('90.5\n-90.5\n-130.342\n58.75\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    calc_dec_deg_to_deg_min_sec(-999., input_data_file='{}'.format(temp_in_file.strpath), output_data_file=temp_out_file.strpath, log_file=temp_log_file)
#    calc_dec_deg_to_deg_min_sec(-999.,input_data_file='{}'.format(temp_in_file.strpath), output_data_file=out_file, log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '90,30,0\n-90,30,0\n-130,20,31\n58,45,0\n'
    expected_log = 'Convert degrees minutes seconds to decimal degrees\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
