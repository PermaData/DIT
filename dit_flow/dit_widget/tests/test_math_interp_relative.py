import pytest
import os

from dit_flow.dit_widget.math_interp_relative import math_interp_relative


def test_math_interp_relative(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'interp_in_file')
    out_log_file = os.path.join(this_dir, 'interp_log')
    out_data_file = os.path.join(this_dir, 'interp_out_file')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    math_interp_relative(-999.0, False, log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
#    math_interp_relative(-999.0, False, log_file=out_log_file,                       output_data_file=out_data_file,                      input_data_file=in_data_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = 'a,1,10.0\n'\
                   'a,2,20.0\n'\
                   'a,3,30.0\n'\
                   'a,4,40.0\n'\
                   'a,5,50.0\n'\
                   'a,6,60.0\n'\
                   'a,7,70.0\n'\
                   'a,8,80.0\n'\
                   'b,1,100.0\n'\
                   'b,2,200.0\n'\
                   'b,3,300.0\n'\
                   'b,4,400.0\n'\
                   'c,1,10\n'\
                   'c,2,-999\n'\
                   'c,3,-999\n'\
                   'c,4,-999\n'

    expected_log = 'Interpolate by Site and relative value\n'\
                   '\tNumber in records: 16\n'\
                   '\tnumber sites: 3 \n'\
                   '\tInterpolate: a\n'\
                   '\tInterpolate: b\n'\
                   '\tNot enough valid points to interpolate c\n'\
                   '\t\tNumber valid points: 1\n'\
                   '\tLast point must be valid to interpolate c\n'\
                   '\t\tLast point: -999.0\n'

    assert expected_out in actual_out
    assert expected_log in actual_log
