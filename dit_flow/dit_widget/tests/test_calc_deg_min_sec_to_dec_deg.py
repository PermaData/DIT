import os

from dit_flow.dit_widget.calc_deg_min_sec_to_dec_deg import calc_deg_min_sec_to_dec_deg


def test_calc_deg_min_sec_to_dec_deg(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('90.0,30.,0.\n-90.0,30.,0.\n-130.0,30.,10.\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    out_file = os.path.join(this_dir, 'test_calc_out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    calc_deg_min_sec_to_dec_deg(-999., input_data_file='{}'.format(temp_in_file.strpath), output_data_file=temp_out_file.strpath, log_file=temp_log_file)
#    calc_deg_min_sec_to_dec_deg(-999., input_data_file='{}'.format(temp_in_file.strpath), output_data_file=out_file,              log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '90.5000000000\n-90.5000000000\n-130.5027770996\n'
    expected_log = 'Convert degrees minutes seconds to decimal degrees\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
