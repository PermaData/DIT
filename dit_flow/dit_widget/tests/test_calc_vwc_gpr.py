import os

from dit_flow.dit_widget.calc_vwc_gpr import calc_vwc_gpr


def test_calc_vwc_gpr(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_file = os.path.join(this_dir, 'vwc.in')
    out_file = os.path.join(this_dir, 'vwc.out')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    calc_vwc_gpr(-999., True, input_data_file=in_file, output_data_file=temp_out_file.strpath, log_file=temp_log_file)
#    calc_vwc_gpr(-999., True, input_data_file=in_file, output_data_file=out_file             , log_file=out_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '12.0,6.25,0.11813916015625\n'\
                   '8.0,14.0625,0.26248123931884765\n'\
                   '6.0,25.0,0.41228125000000004\n'\
                   '4.8,39.0625,0.5428766250610352\n'\
                   '4.0,56.25,0.6620102539062499\n'\
                   '3.4285714285714284,76.5625,0.8394194107055667\n'\
                   '3.0,100.0,1.0\n'\
                   '2.6666666666666665,126.5625,1.0\n'\
                   '2.4,156.25,1.0\n'
    expected_log = 'Calculate VWC given TWTT and ALT\n'\
                   '\t      twtt (ns)        alt (cm) velocity (cm/ns)  dielectric (-)         vwc (-)\n'\
                   '\t     10.0000000      60.0000000      12.0000000       6.2500000       0.1181392\n'\
                   '\t     15.0000000      60.0000000       8.0000000      14.0625000       0.2624812\n'\
                   '\t     20.0000000      60.0000000       6.0000000      25.0000000       0.4122813\n'\
                   '\t     25.0000000      60.0000000       4.8000000      39.0625000       0.5428766\n'\
                   '\t     30.0000000      60.0000000       4.0000000      56.2500000       0.6620103\n'\
                   '\t     35.0000000      60.0000000       3.4285714      76.5625000       0.8394194\n'\
                   '\t     40.0000000      60.0000000       3.0000000     100.0000000       1.0000000\n'\
                   '\t     45.0000000      60.0000000       2.6666667     126.5625000       1.0000000\n'\
                   '\t     50.0000000      60.0000000       2.4000000     156.2500000       1.0000000\n'

    assert expected_out in actual_out
    assert expected_log in actual_log
