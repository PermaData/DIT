from circuits.web import Controller
from dit_gui.create_flow import Create
from dit_gui.templates import Templates


class Update(Controller):

    channel = "/update"

    def GET(self, *args, **kwargs):
        print('IN UPDATE GET:  args: ', args, '  kwargs: ', kwargs)
        this_config = Create.config_translator.config
        print('empty config: ', this_config)
        Create.config_translator.deep_update(this_config, Create.config_translator.read_config(kwargs['config_file_path']))
        this_config = Create.config_translator.config_to_html_vals(this_config)
        print('before return: ', this_config)
        return Templates.serve_template(Create.tpl, configs=Create.configs, config=this_config,
                                        config_file_path=kwargs['config_file_path'],
                                        widget=Create.config_translator.widget)
