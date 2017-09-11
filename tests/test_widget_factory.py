import pytest
import os

from widget_factory import WidgetFactory
from dit_flow.dit_widget.widget_template import widget_template
from dit_flow.manipulation_widget import ManipulationWidget

def test_create_valid_widget():
    factory = WidgetFactory()
    actual = factory.create_widget('widget_template')
    expected = ManipulationWidget()
    print(expected)
    assert isinstance(actual, expected)

def test_add_factory():
    factory = WidgetFactory()
    factory.add_factory('widget_template', )
