from circuits.web import Controller
from dit_gui.templates import Templates
from widget_factory import WidgetFactory, widget_configs_by_type


class Load(Controller):

    tpl = "index-table.html"

    widget_factory = WidgetFactory()
    configs = widget_configs_by_type(widget_factory.loader)
    config_translator = widget_factory.create_widget('config_translator')

    def GET(self, *args, **kwargs):
        the_config = Load.config_translator.config_to_html_vals(Load.config_translator.config)
        print('Starting with config: ', the_config)
        return Templates.serve_template(Load.tpl, configs=Load.configs,
                                        config_file_path=Load.config_translator.config_file_path,
                                        config=the_config,
                                        widget=Load.config_translator.widget)
