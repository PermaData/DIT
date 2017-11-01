from dit_flow.dit_widget.sort_by_columns import sort_by_columns


def test_sort_by_columns(tmpdir):
    temp_in_file = tmpdir.mkdir("sub").join('input_file.csv')
    line_1 = ('1.0, 1.0, 6.0\n')
    line_2 = ('3.0, 2.0, 5.0\n')
    line_3 = ('2.0, 3.0, 4.0\n')
    line_4 = ('2.0, 4.0, 3.0\n')
    line_5 = ('3.0, 5.0, 2.0\n')
    line_6 = ('1.0, 6.0, 1.0\n')
    temp_in_file.write("{}{}{}{}{}{}".format(line_1, line_2, line_3,
                                             line_4, line_5, line_6))
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    sort_by_columns([(1, 'real'), (2, 'real')],
                    log_file=temp_log_file.strpath,
                    output_data_file=temp_out_file.strpath,
                    input_data_file=temp_in_file.strpath)
    actual_out = temp_out_file.read()
    expected_out = "{}{}{}{}{}{}".format(line_1, line_6, line_3,
                                         line_4, line_2, line_5).replace(' ', '')
    assert expected_out == actual_out
