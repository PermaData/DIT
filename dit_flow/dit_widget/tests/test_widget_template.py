import pytest

from dit_flow.dit_widget.widget_template import widget_template

def test_default_dit_arguments(capsys):
    widget_template('arg_1', 'arg_2')
    out, err = capsys.readouterr()
    expected = 'I am a widget. Here are my arguments:\n' \
               '\tinput_data_file = None\n' \
               '\toutput_data_file = None\n' \
               '\tlog_file = None\n' \
               '\tlog_level = 20\n' \
               '\tmethod_arg_1 = arg_1\n' \
               '\tmethod_arg_2 = arg_2\n'
    assert out == expected

def test_missing_required_argument():
    with pytest.raises(TypeError):
        widget_template('arg_1')

def test_writes_to_log_file(tmpdir):
    temp_path = tmpdir.mkdir("sub").join('test.log')
    widget_template('arg_1', 'arg_2', log_file='{}'.format(temp_path.strpath))
    file_out = temp_path.read()
    log_expected = 'log_file = {}'.format(temp_path.strpath)
    arg_1_expected = '\tmethod_arg_1 = arg_1'
    arg_2_expected = '\tmethod_arg_2 = arg_2'
    assert log_expected in file_out
    assert arg_1_expected in file_out
    assert arg_2_expected in file_out
