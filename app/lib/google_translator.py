from logging import getLogger
from django.conf import settings
import requests
from app.exceptions import CloudTranslationParseError

logger = getLogger(__name__)


class GoogleTranslator(object):

    URL = 'https://translation.googleapis.com/language/translate/v2'

    PAYLOAD_FORMAT = {
        'key': settings.GOOGLE_API_KEY,
        'source': 'en',
        'target': 'ja',
        'format': 'text',
    }

    @classmethod
    def _post(cls, payload):
        return requests.post(cls.URL, data=payload, timeout=10)

    @classmethod
    def translate(cls, texts):
        payload = cls.PAYLOAD_FORMAT
        payload['q'] = texts
        res = cls._post(payload)
        response_texts = res.json().get('data', {}).get('translations', [])
        translated_texts = [t.get('translatedText') for t in response_texts]

        if not translated_texts or not all(translated_texts):
            logger.critical(res.text)
            raise CloudTranslationParseError('Response body from Google Cloud Translation was changed.')

        return translated_texts
