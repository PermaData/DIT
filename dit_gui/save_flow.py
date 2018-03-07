from circuits.web import Controller
from dit_gui.create_flow import Create
from dit_gui.templates import Templates


class Save(Controller):

    channel = "/save"

    def POST(self, *args, **kwargs):
        print('save begin post: ', kwargs)
        config_file_path = kwargs['config_file_path']
        this_config = Create.config_translator.config
        Create.config_translator.deep_update(this_config, kwargs) # Create.config_translator.html_to_config_vals(kwargs))
        Create.config_translator.save_config(config_file_path, this_config)
        print('save before return: ', this_config)
        return Templates.serve_template(Create.tpl, configs=Create.configs,
                                        config_file_path=config_file_path,
                                        config=this_config,
                                        widget=Create.config_translator.widget)
