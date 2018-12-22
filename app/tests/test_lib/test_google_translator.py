from unittest.mock import Mock, patch

import requests
from django.conf import settings

from app.exceptions import CloudTranslationParseError
from app.lib.google_translator import GoogleTranslator
from app.tests.base_testcase import BaseTestCase


class GoogleTranslatorTestCase(BaseTestCase):

    @patch('requests.post')
    def test_post(self, m):
        m.return_value = requests.Response()
        result = GoogleTranslator._post({})

        self.assertIsInstance(result, requests.Response)

    def test_translate(self):
        response_json = {
            'data': {
                'translations': [
                    {'translatedText': 'TRANSLATED_TEXT_0'},
                    {'translatedText': 'TRANSLATED_TEXT_1'},
                ],
            }
        }
        response_mock = Mock()
        response_mock.json.return_value = response_json
        GoogleTranslator._post = Mock()
        GoogleTranslator._post.return_value = response_mock

        texts = ['TEXT_0', 'TEXT_1']
        GoogleTranslator.translate(texts)

        GoogleTranslator._post.assert_called_with({
            'q': texts,
            'key': settings.GOOGLE_API_KEY,
            'source': 'en',
            'target': 'ja',
            'format': 'text',
        })

    @patch('app.lib.google_translator.logger')
    def test_translate_error(self, _):
        response_json = {
            'INVALID_KEY': {
                'translations': [
                    {'translatedText': 'TRANSLATED_TEXT_0'},
                ],
            }
        }
        response_mock = Mock()
        response_mock.json.return_value = response_json
        GoogleTranslator._post = Mock()
        GoogleTranslator._post.return_value = response_mock

        texts = ['TEXT_0']
        with self.assertRaises(CloudTranslationParseError):
            GoogleTranslator.translate(texts)
