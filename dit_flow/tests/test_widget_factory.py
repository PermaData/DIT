import pytest

from dit_flow.widget_factory import WidgetFactory
from dit_flow.dit_widget.widget_template import widget_template
from dit_flow.manipulation_widget import ManipulationWidget


def test_add_factory():
    factory = WidgetFactory()
    factory.addFactory('widget_template', )

def test_create_valid_widget():
    factory = WidgetFactory()
    actual = factory.createWidget('ManipulationWidget')
    expected = ManipulationWidget()
    print(expected)
    assert isinstance(actual, expected)