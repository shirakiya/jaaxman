import json
import os

from django.conf import settings


class Webpack(object):

    ASSETS_HOST_PRODUCTION = 'https://s3-ap-northeast-1.amazonaws.com/jaaxman-production-public/js/bundle/'
    ASSETS_HOST_DEVELOPMENT = 'http://localhost:8001/assets/'

    def __init__(self):
        self.assets_base_url = self._get_assets_base_url()

    def _get_assets_base_url(self):
        if settings.RUN_MODE == settings.RUN_MODE_PRODUCTION:
            return self.ASSETS_HOST_PRODUCTION
        else:
            return self.ASSETS_HOST_DEVELOPMENT

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
