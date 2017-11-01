import pytest
import os
from widget_loader import WidgetLoader


def test_find_valid_widget():
    loader = WidgetLoader()
    (config_path, method_path) = loader.find_widget('math_add_constant')
    expected_config_path = os.path.join(loader.widget_dir, 'math_add_constant.yaml')
    expected_method_path = os.path.join(loader.widget_dir, 'math_add_constant.py')
    assert config_path == expected_config_path
    assert method_path == expected_method_path
