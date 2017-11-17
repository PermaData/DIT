from dit_flow.dit_widget.math_square import math_square


def test_math_square(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    temp_in_file.write('1.0\n2.0\n-999.99\n4.0\n0A\n0B\nXX\n')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    math_square(-999.99, log_file='{}'.format(temp_log_file.strpath),
                output_data_file='{}'.format(temp_out_file.strpath),
                input_data_file='{}'.format(temp_in_file.strpath))
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1.00\n4.00\n-999.99\n16.00\n-999.99\n-999.99\n-999.99'
    expected_log = 'Squares values in column\n'\
                   '    Records with non-number entry types:\n'\
                   '         Record                Value\n'\
                   '              5                   0A\n'\
                   '              6                   0B\n'\
                   '              7                   XX\n'\
                   '    Total number of non-number entries: 3\n'
    assert expected_out in actual_out
    assert expected_log in actual_log
