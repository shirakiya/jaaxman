import os

from app.lib.util.webpack import Webpack
# from django.test import override_settings
from app.tests.base_testcase import BaseTestCase


class WebpackTestCase(BaseTestCase):

    def setUp(self):
        self.webpack = Webpack()

    def test_get_asserts_base_url(self):
        result = self.webpack._get_assets_base_url()

        self.assertEqual(result, self.webpack.URL_WEBPACK_DEV_SERVER)

    def test_get_manifest(self):
        dummy_path = os.path.join(self.get_test_files_dir(), 'manifest.json')
        with self.settings(MANIFEST_PATH=dummy_path):
            result = self.webpack._get_manifest()

            self.assertEqual(result, {'index.js': 'index-test.bundle.js'})

    def test_get_manifest_when_not_exists(self):
        dummy_path = os.path.join(self.get_test_files_dir(), 'not_exists_manifest.json')
        with self.settings(MANIFEST_PATH=dummy_path):
            result = self.webpack._get_manifest()

            self.assertEqual(result, {})
