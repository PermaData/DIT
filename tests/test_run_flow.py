import pytest
import os
import numpy as np

from collections import OrderedDict
from run_flow import RunFlow

config_path = os.path.join(os.getcwd(), 'dit_flow', 'dit_widget', 'tests', 'test_config.yml')


def test_setup_utilities():
    actual = RunFlow(config_path)
    actual.setup_utilities()
    assert actual.widget_factory
    assert actual.file_manager
    assert actual.file_reader
    assert actual.variable_mapper


def test_read_input_data(tmpdir):
    datafile = tmpdir.mkdir('input').join('data_file')
    line_1 = 'column 1,column_2,Column3, Column  4\n'
    line_2 = "'fred', 'ginger', 'elf', 'santa'\n"
    line_3 = "1.00, 2.13, na, -999.99\n"
    datafile.write("{}{}{}".format(line_1, line_2, line_3))
    flow = RunFlow(config_path)
    flow.setup_utilities()
    actual = flow.read_input_data(str(datafile), 2)
    assert len(actual) == 3
    assert actual[0] == line_1.replace('\n', '').split(',')
    assert actual[1] == line_2.replace('\n', '').split(',')
    assert actual[2] == line_3.replace('\n', '').split(',')


def test_setup_input_manipulations():
    expected_args = OrderedDict([

        ('method_arg_1', 'fred'),
        ('method_arg_2', 'ginger')
    ])
    actual = RunFlow(config_path)
    actual.setup_input_manipulations()
    assert len(actual.input_manipulations) == 1
    actual_widget = actual.input_manipulations[0]
    assert actual_widget.__class__.__name__ == 'WidgetTemplate'
    assert actual_widget.widget_method.__name__ == 'widget_template'
    assert actual_widget.input_args == expected_args
    assert actual_widget.do_it == True


def test_setup_output_manipulations():
    expected_args_1 = OrderedDict([
        ('method_arg_1', 'fred'),
        ('method_arg_2', 'ginger')
    ])
    expected_args_2 = OrderedDict([
        ('constant', 1.0),
        ('missing_value', -999.99)
    ])
    expected_args_3 = OrderedDict([
        ('method_arg_1', 'elf'),
        ('method_arg_2', 'santa')
    ])
    actual = RunFlow(config_path)
    actual.setup_output_manipulations()
    assert len(actual.output_manipulations) == 3
    actual_widget_1 = actual.output_manipulations[0]
    assert actual_widget_1.__class__.__name__ == 'WidgetTemplate'
    assert actual_widget_1.widget_method.__name__ == 'widget_template'
    assert actual_widget_1.input_args == expected_args_1
    assert actual_widget_1.do_it == True

    actual_widget_2 = actual.output_manipulations[1]
    assert actual_widget_2.__class__.__name__ == 'AddConstant'
    assert actual_widget_2.widget_method.__name__ == 'add_constant'
    assert actual_widget_2.input_args == expected_args_2
    assert actual_widget_2.do_it == False

    actual_widget_3 = actual.output_manipulations[2]
    assert actual_widget_3.__class__.__name__ == 'WidgetTemplate'
    assert actual_widget_3.widget_method.__name__ == 'widget_template'
    assert actual_widget_3.input_args == expected_args_3
    assert actual_widget_3.do_it == True


def test_do_input_manipulations():
    flow = RunFlow(config_path)
    pass


def test_do_output_manipulations():
    flow = RunFlow(config_path)
    pass


def test_write_output_file(tmpdir):
    datafile = tmpdir.mkdir('output').join('data_file')
    line_1 = ['column 1', 'column_2', 'Column3', 'Column  4']
    line_2 = ['fred', 'ginger', 'elf', 'santa']
    line_3 = [1.00, 2.13, 'na', -999.99]
    input_data = [line_1, line_2, line_3]
    flow = RunFlow(config_path)
    flow.setup_utilities()
    flow.write_output_file(str(datafile), input_data, 'test.log')
    actual = datafile.read()
    print(actual)
    assert len(actual) == 3
    assert actual[0] == line_1.replace('\n', '').split(',')
    assert actual[1] == line_2.replace('\n', '').split(',')
    assert actual[2] == line_3.replace('\n', '').split(',')
