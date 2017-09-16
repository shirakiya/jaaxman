from django import template
from app.lib.util.webpack import Webpack

register = template.Library()
webpack = Webpack()


@register.simple_tag
def webpack_js(base_name):
    return webpack.get_js_src(base_name)
