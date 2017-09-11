import pytest
import os
from dit_flow.flow_widget import FlowWidget, type_from_config, inputs_from_config, description_from_config

def test_type_from_config():
    widget_dir = os.path.join(os.getcwd(), 'dit_flow', 'dit_widget')
    config_file = os.path.join(widget_dir, 'widget_template.yaml')
    actual = type_from_config(config_file)
    expected = 'ManipulationWidget'
    assert actual == expected

def test_inputs_from_config():
    widget_dir = os.path.join(os.getcwd(), 'dit_flow', 'dit_widget')
    config_file = os.path.join(widget_dir, 'widget_template.yaml')
    actual = inputs_from_config(config_file)
    expected = [('method_arg_1', 'string'), ('method_arg_2', 'integer')]
    assert actual == expected

def test_description_from_config():
    widget_dir = os.path.join(os.getcwd(), 'dit_flow', 'dit_widget')
    config_file = os.path.join(widget_dir, 'widget_template.yaml')
    expected = 'This is a template widget designed as an example of implementing a DIT widget.'
    actual = description_from_config(config_file)
    assert actual == expected
