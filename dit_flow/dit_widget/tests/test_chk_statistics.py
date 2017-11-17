import os

from dit_flow.dit_widget.chk_statistics import chk_statistics


def test_chk_statistics(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_stats.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    chk_statistics(-999.0, log_file='{}'.format(temp_log_file.strpath),
                   input_data_file=in_data_file)
#   chk_statistics(-999.0,log_file=out_log_file,
#                  input_data_file=in_data_file)
    actual_log = temp_log_file.read()
    expected_log = 'Count distinct values\n'\
                   'Total number =3\n'\
                   'Col      nrec      Mean     Stdev    Median       Min       Max\n'\
                   '1        16     4.065     2.414     3.645     0.920     9.000\n'\
                   '2        17     1.006     0.483     0.990     0.170     1.790\n'\
                   '3        16    39.955    32.868    37.030     1.600    96.420\n'
    assert expected_log in actual_log
