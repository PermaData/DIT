import os

from dit_flow.dit_widget.make_kml_wall import make_kml_wall


def test_make_kml_wall(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_kml_wall.in')
    out_log_file = os.path.join(this_dir, 'test_print_log')
    out_data_file = os.path.join(this_dir, 'test_out.kml')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    make_kml_wall(-999., 1., log_file='{}'.format(temp_log_file.strpath), output_data_file='{}'.format(temp_out_file.strpath), input_data_file=in_data_file)
    make_kml_wall(-999., 1., log_file=out_log_file,                       output_data_file=out_data_file,                      input_data_file=in_data_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    expected_out = '1,Junk\n2,Junk\n3,Junk\n4,Junk\n'\
                   '5,Junk\n6,test\n1,Junk\n2,Junk\n'\
                   '3,Junk\n4,Junk\n5,Junk\n6,test\n'
    expected_log = 'Make kml wall file: {}\n'.format(out_log_file)
   # assert expected_out in actual_out
   # assert expected_log in actual_log
