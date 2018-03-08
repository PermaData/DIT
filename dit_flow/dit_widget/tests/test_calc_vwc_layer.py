import os

from dit_flow.dit_widget.calc_vwc_layer import calc_vwc_layer


def test_calc_vwc_layer(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_file = os.path.join(this_dir, 'vwc_layer.in')
    out_file = os.path.join(this_dir, 'vwc_layer.out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    calc_vwc_layer(-999., True, input_data_file=in_file, output_data_file=temp_out_file.strpath, log_file=temp_log_file)
#    calc_vwc_layer(-999., True, input_data_file=in_file, output_data_file=out_file             , log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '0.5,0.5,0.5000000000000001\n'\
                   '0.4,0.65,0.5000000000000001\n'\
                   '0.3,0.7999999999999999,0.5000000000000001\n'\
                   '0.1,1.0999999999999999,0.5000000000000001\n'\
                   '0.1,0.85,0.55\n'\
                   '0.1,0.6,0.6000000000000001\n'

    expected_log = 'calculate VWC for 3 layers given 3 depths and three depth average VWC\n'\
                   '\t             d3          V_0_d1          V_0_d2          V_0_d3            VWC1            VWC2            VWC3\n'\
                   '\t     60.0000000       0.5000000       0.5000000       0.5000000       0.5000000       0.5000000       0.5000000\n'\
                   '\t     60.0000000       0.4000000       0.5000000       0.5000000       0.4000000       0.6500000       0.5000000\n'\
                   '\t     60.0000000       0.3000000       0.5000000       0.5000000       0.3000000       0.8000000       0.5000000\n'\
                   '\t     60.0000000       0.1000000       0.5000000       0.5000000       0.1000000       1.1000000       0.5000000\n'\
                   '\t     60.0000000       0.1000000       0.4000000       0.5000000       0.1000000       0.8500000       0.5500000\n'\
                   '\t     60.0000000       0.1000000       0.3000000       0.5000000       0.1000000       0.6000000       0.6000000\n'

    assert expected_out in actual_out
    assert expected_log in actual_log
