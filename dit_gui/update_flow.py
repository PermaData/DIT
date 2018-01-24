from dit_gui.load_flow import Load
from dit_gui.templates import Templates


class Update(Load):

    channel = "/update"
    this_config = Load.config_translator.config

    def POST(self, *args, **kwargs):
        print('begin update post: ', self.this_config)
        Load.config_translator.read_config(kwargs['flow_name'])
        Load.config_translator.deep_update(self.this_config, kwargs)
        print('before return: ', self.this_config)
        return Templates.serve_template(Load.tpl, configs=Load.configs, config=self.this_config,
                                        widget=Load.config_translator.widget)
