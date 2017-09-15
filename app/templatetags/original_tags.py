from django import template
from django.conf import settings

register = template.Library()


def get_assets_url():
    if settings.RUN_MODE == settings.RUN_MODE_PRODUCTION:
        return ''  # TODO: fix
    else:
        return 'http://localhost:8001/assets/'


@register.simple_tag
def webpack_js(base_name):
    assets_url = get_assets_url()
    bundle_name = settings.MANIFEST.get(base_name, '')

    return assets_url + bundle_name
