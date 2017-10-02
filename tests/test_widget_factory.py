import pytest
import os

from widget_factory import WidgetFactory, WidgetCreateException, inputs_from_config, type_from_config, description_from_config, create_widget_class
from widget_loader import WidgetLoader
from dit_flow.manipulation_widget import ManipulationWidget
from dit_flow.utility_widget import UtilityWidget


def test_create_manipulation_widget():
    factory = WidgetFactory()
    actual = factory.create_widget('widget_template')
    expected = ManipulationWidget
    assert isinstance(actual, expected)


def test_create_utility_widget():
    factory = WidgetFactory()
    actual = factory.create_widget('config_translator')
    expected = UtilityWidget
    assert isinstance(actual, expected)

def test_type_from_config():
    widget_dir = os.path.join(os.getcwd(), 'dit_flow', 'dit_widget')
    config_file = os.path.join(widget_dir, 'widget_template.yaml')
    actual = type_from_config(config_file)
    expected = ManipulationWidget
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

def test_create_widget_class():
    loader = WidgetLoader()
    actual = create_widget_class('widget_template', loader)
    assert actual().__class__.__name__ == 'WidgetTemplate'

def test_create_nonexistent_widget_class():
    loader = WidgetLoader()
    with pytest.raises(WidgetCreateException):
        create_widget_class('fake_widget', loader)
