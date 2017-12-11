import os

from dit_flow.dit_widget.chk_count_distinct_double import chk_count_distinct_double


def test_chk_count_distinct_double(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_txt2.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_count_distinct_double('true', log_file='{}'.format(temp_log_file.strpath), input_data_file=in_data_file)
#    chk_count_distinct_double('true', log_file=out_log_file,                       input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Count distinct values\n'\
                   '\tTotal number =20\n'\
                   '  Num                              Col A Value                 '\
                   '             Col B Value     number    Percent\n'\
                   '    1                                     Crap                 '\
                   '                    blue          3     15.000\n'\
                   '    2                                     Crap                 '\
                   '                     red          4     20.000\n'\
                   '    3                                  Garbage                 '\
                   '                   green          3     15.000\n'\
                   '    4                                  Garbage                 '\
                   '                  orange          3     15.000\n'\
                   '    5                                     junk                 '\
                   '                   green          2     10.000\n'\
                   '    6                                     junk                 '\
                   '                  orange          2     10.000\n'\
                   '    7                                       na                 '\
                   '                    blue          2     10.000\n'\
                   '    8                                       na                 '\
                   '                     red          1      5.000\n'
    assert expected_log in actual_log
