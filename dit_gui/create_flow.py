from circuits.web import Controller
from dit_gui.templates import Templates
from widget_factory import WidgetFactory, widget_configs_by_type


class Create(Controller):

    tpl = "index-table.html"

    widget_factory = WidgetFactory()
    configs = widget_configs_by_type(widget_factory.loader)
    config_translator = widget_factory.create_widget('config_translator')

    def GET(self, *args, **kwargs):
        print('In CREATE GET')
        the_config = Create.config_translator.config
        html_config = Create.config_translator.config_to_html_vals(the_config)
        print('Starting with config: ', html_config)
        return Templates.serve_template(Create.tpl, configs=Create.configs,
                                        config_file_path=Create.config_translator.config_file_path,
                                        config=html_config,
                                        widget=Create.config_translator.widget)
