import os
from unittest.mock import Mock, patch
from django.core.management import call_command
from jaaxman.exceptions import EnvironmentVariableNotDefineError
from app.tests.base_testcase import BaseTestCase
from app.models import Paper


class FetchRssTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject_0 = self.creation.rss_fetch_subject(name='NAME_0')
        self.rss_fetch_subject_1 = self.creation.rss_fetch_subject(name='NAME_1')

    @patch('app.management.commands.fetchrss.Slack.notify_fetchrss')
    @patch('app.management.commands.fetchrss.logger')
    @patch('app.management.commands.fetchrss.ArxivRss.fetch_and_save')
    def test_slack(self, m_fetch_and_save, m_logger, m_notify_fetchrss):
        os.environ['SLACK_URL'] = ''
        m_fetch_and_save.return_value = []

        with self.assertRaises(EnvironmentVariableNotDefineError):
            call_command('fetchrss')

    @patch('app.management.commands.fetchrss.Command._slack')
    @patch('app.management.commands.fetchrss.logger')
    @patch('app.management.commands.fetchrss.ArxivRss.fetch_and_save')
    def test_handle(self, m_fetch_and_save, m_logger, m_slack):
        slack_mock = Mock()
        m_fetch_and_save.return_value = [Paper(), Paper()]
        m_slack.return_value = slack_mock
        call_command('fetchrss')

        m_logger.info.assert_called_with('\x1b[32;1mSuccessfully fetch and save 4 papers from RSS.\x1b[0m')
        slack_mock.notify_fetchrss.assert_called_with('Successfully fetch and save 4 papers from RSS.')
