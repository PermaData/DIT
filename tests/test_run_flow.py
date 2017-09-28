import pytest
import os
import numpy as np

from numpy import array
from collections import OrderedDict
from pathlib import Path
from run_flow import RunFlow

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           '../dit_flow', 'dit_widget', 'tests',
                           'test_config.yml')


def create_input_data():
    line_1 = ['column 1', 'column_2', 'Column3', 'Column 4']
    line_2 = ['fred', 'ginger', 'elf', 'santa']
    line_3 = [1.00, 2.13, 'na', -999.99]
    input_data = [line_1, line_2, line_3]
    return input_data


def test_setup_utilities():
    actual = RunFlow(config_path)
    actual.setup_utilities()

    assert actual.widget_factory
    assert actual.file_manager
    assert actual.file_reader
    assert actual.variable_mapper


def test_read_input_data(tmpdir):
    expected_line_1 = ['column 1', 'column_2', 'Column3', 'Column  4']
    expected_line_2 = ['fred', '"ginger"', 'elf', 'santa']
    expected_line_3 = ['1.00', '2.13', 'na', '-999.99']

    datafile = tmpdir.mkdir('input').join('data_file')
    line_1 = 'column 1,column_2,Column3, Column  4\n'
    line_2 = "'fred', \"ginger\", 'elf', 'santa'\n"
    line_3 = "1.00, 2.13, na, -999.99\n"
    datafile.write("{}{}{}".format(line_1, line_2, line_3))

    flow = RunFlow(config_path)
    flow.setup_utilities()
    actual = flow.read_input_data(str(datafile), 'test.log')

    actual_list = actual.tolist()
    assert len(actual_list) == 3
    assert actual_list[0] == expected_line_1
    assert actual_list[1] == expected_line_2
    assert actual_list[2] == expected_line_3


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


def test_subset_data_with_header():
    expected = np.array([['column 1', 'Column3'], ['fred', 'elf'], [1.00, 'na']], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.subset_data(np.array(input_data, dtype=object), [1, 3], with_header=True)

    np.testing.assert_array_equal(actual, expected)


def test_subset_data_without_header():
    expected = np.array([['fred', 'elf'], [1.00, 'na']], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.subset_data(np.array(input_data, dtype=object), [1, 3])

    np.testing.assert_array_equal(actual, expected)

def test_subset_one_column():
    input_data = [['column 1', 'column_2', 'Column3', 'Column 4'],
                  ['fred', 'ginger', 'elf', 'santa'],
                  [1.00, 2.13, 'na', -999.99],
                  [3.00,4.0005,5,6]]
    expected = np.array([['column 1'],
                         ['fred'],
                         [1.00],
                         [3.00]], dtype=object)

    flow = RunFlow(config_path)

    actual = flow.subset_data(np.array(input_data, dtype=object), [1], with_header=True)

    np.testing.assert_array_equal(actual, expected)



def test_subset_all_data_with_header():
    expected = np.array([['column 1', 'column_2', 'Column3', 'Column 4'],
                         ['fred', 'ginger', 'elf', 'santa'],
                         [1.00, 2.13, 'na', -999.99]], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.subset_data(np.array(input_data, dtype=object), ['all'], with_header=True)

    np.testing.assert_array_equal(actual, expected)


def test_subset_all_data_without_header():
    expected = np.array([['fred', 'ginger', 'elf', 'santa'],
                         [1.00, 2.13, 'na', -999.99]], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.subset_data(np.array(input_data, dtype=object), ['all'])

    np.testing.assert_array_equal(actual, expected)


def test_replace_data_with_header():
    expected = np.array([['new col 1', 'column_2', 'NewColumn3', 'Column 4'],
                         ['ethel', 'ginger', 'reindeer', 'santa'],
                         [0.000003, 2.13, 5055.3042, -999.99]], dtype=object)
    new_columns = np.array([['new col 1', 'NewColumn3'], ['ethel', 'reindeer'], [0.000003, 5055.3042]], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.replace_data(np.array(input_data, dtype=object), new_columns, [1, 3], True)

    np.testing.assert_array_equal(actual, expected)


def test_replace_data_without_header():
    expected = np.array([['column 1', 'column_2', 'Column3', 'Column 4'],
                         ['ethel', 'ginger', 'reindeer', 'santa'],
                         [0.000003, 2.13, 5055.3042, -999.99]], dtype=object)
    new_columns = np.array([['ethel', 'reindeer'], [0.000003, 5055.3042]], dtype=object)

    flow = RunFlow(config_path)
    input_data = create_input_data()

    actual = flow.replace_data(np.array(input_data, dtype=object), new_columns, [1, 3])

    np.testing.assert_array_equal(actual, expected)


def test_do_input_manipulations():
    flow = RunFlow(config_path)
    pass


def test_do_output_manipulations():
    flow = RunFlow(config_path)
    pass


def test_write_output_file():
    expected = "'column 1','column_2','Column3','Column 4'\n" \
    "'fred','ginger','elf','santa'\n" \
    "1.0,2.13,'na',-999.99\n"

    output_directory = os.path.dirname(os.path.realpath(__file__))
    datafile = os.path.join(output_directory, 'data_file')
    input_data = create_input_data()

    flow = RunFlow(config_path)
    flow.setup_utilities()
    flow.write_output_file(datafile, input_data, 'test.log')
    with open(datafile, 'r') as readfile:
        actual = readfile.read()

    assert actual == expected
