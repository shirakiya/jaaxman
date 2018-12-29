import json
import os

from django.conf import settings


class Webpack(object):

    ASSETS_HOST_PRODUCTION = 'https://s3-ap-northeast-1.amazonaws.com/jaaxman-production-public/js/bundle/'
    ASSETS_HOST_DEVELOPMENT = os.getenv('ASSETS_BASE_URL', 'http://localhost:8001/assets/')

    def __init__(self):
        self.assets_base_url = self._get_assets_base_url()
        self._manifest = None

    @property
    def manifest(self):
        if not self._manifest or settings.RUN_MODE == settings.RUN_MODE_DEVELOPMENT:
            self._manifest = self._get_manifest()
            return self._manifest

        return self._manifest

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

    def get_src(self, base_name):
        bundle_name = self.manifest.get(base_name, '')

        return self.assets_base_url + bundle_name
