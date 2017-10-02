import os
import pytest

from dit_flow.dit_widget.config_translator import ConfigTranslator

base_dir = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(base_dir, 'test_config.yml')


def test_get_input_files():
    config_trans = ConfigTranslator()
    config_trans.read_config(config_file)
    data_dir = os.path.join(base_dir, 'test_data_files')
    config_trans.config['input']['data_directory'] = data_dir
    expected = []
    for cnt in range(1, 7):
        file_name = 'file_' + str(cnt) + '.csv'
        if cnt < 3:
            file_path = os.path.join(data_dir, file_name)
        elif cnt == 3:
            file_path = os.path.join(data_dir, 'two', file_name)
        else:
            file_path = os.path.join(data_dir, 'two', 'multi', file_name)
        expected.append(file_path)
    actual = config_trans.get_input_files()
    assert actual.sort() == expected.sort()


def test_get_variable_map():
    config_trans = ConfigTranslator()
    config_trans.read_config(config_file)
    actual = config_trans.get_variable_map()
    expected = './example_data/variable_map.dat'
    assert actual == expected

def test_get_reader_widget():
    config_trans = ConfigTranslator()
    config_trans.read_config(config_file)
    actual = config_trans.get_reader_widget()
    expected = 'read_csv_file'
    assert actual == expected

def test_get_missing_values():
    config_trans = ConfigTranslator()
    config_trans.read_config(config_file)
    actual = config_trans.get_missing_values()
    expected = [-999.99, -999.0]
    assert actual == expected

def test_get_missing_characters():
    config_trans = ConfigTranslator()
    config_trans.read_config(config_file)
    actual = config_trans.get_missing_characters()
    expected = ['na']
    assert actual == expected
