from dit_gui.load_flow import Load
from dit_gui.templates import Templates


class Add(Load):

    channel = "/add"
    this_config = {}

    def POST(self, *args, **kwargs):
        print('add begin post: ', self.this_config)
        Load.config_translator.deep_update(self.this_config, Load.config_translator.config)
        Load.config_translator.deep_update(self.this_config, kwargs)
        print('add before return: ', self.this_config)
        return Templates.serve_template(Load.tpl, configs=Load.configs,
                config=self.this_config, widget=Load.config_translator.widget)
