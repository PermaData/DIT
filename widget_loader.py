import os

from os.path import dirname
from circuits import Loader

class WidgetLoader(Loader):

    def init(self, channel=Loader.channel):
        base_dir = os.getcwd() # dirname(__file__)
        flow_dir = os.path.join(base_dir, 'dit_flow')
        widget_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget')
        common_dir = os.path.join(base_dir, 'dit_flow', 'dit_widget', 'common')
        print('directory: ', base_dir)
        print('widget directory: ', widget_dir)
        print('flow dir: ', flow_dir)
        self._loader = Loader(paths=[base_dir, flow_dir, widget_dir, common_dir])

    @property
    def loader(self):
        return self._loader
