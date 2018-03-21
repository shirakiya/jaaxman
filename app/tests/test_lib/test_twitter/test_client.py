from unittest.mock import Mock, patch
from jaaxman.exceptions import EnvironmentVariableNotDefineError
from app.tests.base_testcase import BaseTestCase
from app.lib.twitter import Twitter


class TwitterTestCase(BaseTestCase):

    def _create_valid_twitter(self, settings_mock):
        settings_mock.TWITTER_CONSUMER_KEY = 'TWITTER_CONSUMER_KEY'
        settings_mock.TWITTER_CONSUMER_SECRET = 'TWITTER_CONSUMER_SECRET'
        settings_mock.TWITTER_ACCESS_TOKEN_KEY = 'TWITTER_ACCESS_TOKEN_KEY'
        settings_mock.TWITTER_ACCESS_TOKEN_SECRET = 'TWITTER_CONSUMER_SECRET'

        return Twitter()

    @patch('app.lib.twitter.client.settings')
    def test_validate_credentials_if_not_defined(self, m_settings):
        m_settings.TWITTER_CONSUMER_KEY = ''
        m_settings.TWITTER_CONSUMER_SECRET = ''
        m_settings.TWITTER_ACCESS_TOKEN_KEY = ''
        m_settings.TWITTER_ACCESS_TOKEN_SECRET = ''

        with self.assertRaises(EnvironmentVariableNotDefineError) as cm:
            Twitter()

        self.assertEqual(
            'Not defined TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET'
            ',TWITTER_ACCESS_TOKEN_KEY,TWITTER_ACCESS_TOKEN_SECRET.',
            str(cm.exception))

    @patch('app.lib.twitter.client.settings')
    def test_init(self, m_settings):
        twitter = self._create_valid_twitter(m_settings)

        self.assertIsInstance(twitter, Twitter)

    @patch('app.lib.twitter.client.settings')
    def test_post_tweet(self, m_settings):
        twitter = self._create_valid_twitter(m_settings)
        twitter._api = Mock()
        twitter.post_tweet('TEXT')

        twitter._api.PostUpdate.assert_called_with('TEXT')
