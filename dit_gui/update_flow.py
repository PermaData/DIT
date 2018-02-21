from dit_gui.load_flow import Load
from dit_gui.templates import Templates


class Update(Load):

    channel = "/update"
    this_config = None

    def POST(self, *args, **kwargs):
        print('begin update post: ', self.this_config)
        Load.config_translator.config_file_path = kwargs['config_file_path']
        self.this_config = Load.config_translator.read_config(Load.config_translator.config_file_path)
        # Load.config_translator.deep_update(self.this_config, Load.config_translator.html_to_config_vals(kwargs))
        # self.this_config = Load.config_translator.config_to_html_vals(self.this_config)
        print('before return: ', self.this_config)
        return Templates.serve_template(Load.tpl, configs=Load.configs, config=self.this_config,
                                        widget=Load.config_translator.widget)
