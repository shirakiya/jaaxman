import os
import json
from django.conf import settings


class Webpack(object):

    URL_WEBPACK_DEV_SERVER = 'http://localhost:8001/assets/'

    def __init__(self):
        self.assets_base_url = self._get_assets_base_url()

    def _get_assets_base_url(self):
        if settings.RUN_MODE == settings.RUN_MODE_PRODUCTION:
            return ''  # TODO: fix
        else:
            return self.URL_WEBPACK_DEV_SERVER

    def _get_manifest(self):
        manifest = {}
        if os.path.exists(settings.MANIFEST_PATH):
            with open(settings.MANIFEST_PATH, 'r') as f:
                manifest = json.load(f)
        return manifest

    def get_js_src(self, base_name):
        manifest = self._get_manifest()
        bundle_name = manifest.get(base_name, '')

        return self.assets_base_url + bundle_name
