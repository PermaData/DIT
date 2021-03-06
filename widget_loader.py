import os

from circuits import Loader
from itertools import chain
from pathlib import Path


class WidgetLoader(Loader):

    def __init__(self, channel=Loader.channel):
        super(WidgetLoader, self).__init__(channel)
        base_dir = os.path.dirname(os.path.realpath(__file__))
        flow_dir = os.path.join(base_dir, 'dit_flow')
        self._widget_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget')
        self._widget_dir_2 = os.path.join(base_dir, 'dit_flow', 'done_widget')
        common_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget', 'common')
        self._loader = Loader(paths=[base_dir, flow_dir, self.widget_dir, self._widget_dir_2, common_dir])

    @property
    def loader(self):
        return self._loader

    @property
    def widget_dir(self):
        return self._widget_dir

    def find_all_widget_configs(self):
        widget_path = Path(self._widget_dir)
        widget_configs = []
        for entry in widget_path.iterdir():
            if str(entry).endswith('.yaml'):
                widget_configs.append(entry)
        return widget_configs

    def find_widget(self, widget_name):
        config_file = widget_name + ".yaml"
        method_file = widget_name + ".py"
        found_config = False
        found_method = False
        widget_files = (None, None)
        paths = (self.widget_dir, self._widget_dir_2)
        for root, dirs, files in chain.from_iterable(os.walk(path, topdown=False) for path in paths):
            if config_file in files:
                config_path = os.path.join(root, config_file)
                found_config = True
            if method_file in files:
                method_path = os.path.join(root, method_file)
                found_method = True
            if found_config and found_method:
                widget_files = (config_path, method_path)
                break
        return widget_files
