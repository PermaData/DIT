import mako
import os

from mako.lookup import TemplateLookup

template_dirs = [os.path.join(os.path.dirname(__file__), "tpl")]
#    os.path.join(os.path.dirname(__file__), "flow", "tpl"),
#    os.path.join(os.path.dirname(__file__), "step", "tpl"),
#    os.path.join(os.path.dirname(__file__), "widget", "tpl")]


class Templates():
    print('template dirs: ', template_dirs)

    templates = TemplateLookup(
        directories=template_dirs,
        module_directory="/tmp",
        output_encoding="utf-8"
    )

    @classmethod
    def serve_template(cls, templatename, **kwargs):
        try:
            mytemplate = cls.templates.get_template(templatename)
            return mytemplate.render(**kwargs)
        except:
            return mako.exceptions.html_error_template().render()
