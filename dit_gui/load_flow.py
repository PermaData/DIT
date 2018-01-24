from circuits.web import Controller
from dit_gui.templates import Templates
from widget_factory import WidgetFactory, widget_configs_by_type


class Load(Controller):

    tpl = "index-table.html"

    widget_factory = WidgetFactory()
    configs = widget_configs_by_type(widget_factory.loader)
    config_translator = widget_factory.create_widget('config_translator')

    def GET(self, *args, **kwargs):
        return Templates.serve_template(Load.tpl, configs=Load.configs,
                config=Load.config_translator.config,
                widget=Load.config_translator.widget)
