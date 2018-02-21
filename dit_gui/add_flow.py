from dit_gui.load_flow import Load
from dit_gui.templates import Templates


class Add(Load):

    channel = "/add"
    this_config = {}

    def GET(self, *args, **kwargs):
        print('In add.get')

    def POST(self, *args, **kwargs):
        print('add begin post: ', self.this_config)
        Load.config_translator.config_file_path = kwargs['config_file_path']
        Load.config_translator.deep_update(self.this_config, Load.config_translator.html_to_config_vals(kwargs))
        Load.config_translator.save_fow(self.this_config)
        print('add before return: ', self.this_config)
        return Templates.serve_template(Load.tpl, configs=Load.configs,
                                        config_file_path=Load.config_translator.config_file_path,
                                        config=self.this_config,
                                        widget=Load.config_translator.widget)
