import os

from dit_flow.dit_widget.utm_to_latlong import utm_to_latlong


def test_utm_to_latlong(tmpdir):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    in_data_file = os.path.join(this_dir, 'test_utm_to_latlong.in')
    temp_out_file = tmpdir.mkdir("out").join('output_file.csv')
    temp_log_file = tmpdir.mkdir("log").join('log_file.txt')
    utm_to_latlong(input_data_file=in_data_file,
                   output_data_file=temp_out_file.strpath,
                   log_file=temp_log_file)
    actual_out = temp_out_file.read()
    actual_log = temp_log_file.read()
    print(actual_out)
    print(actual_log)
    expected_out_file = os.path.join(this_dir, 'test_utm_to_latlong.latlong.expected')
    expected_log_file = os.path.join(this_dir, 'test_utm_to_latlong.log.expected')
    with open(expected_out_file) as open_out, open(expected_log_file) as open_log:
        expected_out = open_out.read()
        expected_log = open_log.read()

    assert expected_out in actual_out

    for expected_line in expected_log:
        assert expected_line in actual_log
