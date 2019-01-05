from django import template

from app.lib.util.webpack import Webpack

register = template.Library()
webpack_util = Webpack()


@register.simple_tag
def webpack(base_name):
    return webpack_util.get_src(base_name)
