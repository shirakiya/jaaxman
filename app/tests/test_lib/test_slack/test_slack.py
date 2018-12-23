from unittest.mock import patch

from app.lib.slack import Slack
from app.tests.base_testcase import BaseTestCase


class SlackTestCase(BaseTestCase):

    def setUp(self):
        dummy_url = 'DUMMY_URL'
        self.slack = Slack(dummy_url)

    @patch('app.lib.slack.slack.slackweb.Slack.notify')
    def test_notify(self, m_notify):
        payload = {'test': 'TEST'}
        self.slack.notify(payload)

        m_notify.assert_called_with(test='TEST')

    @patch('app.lib.slack.slack.Slack.notify')
    def test_notify_fetchrss(self, m_notify):
        message = 'TEST MESSAGE'
        self.slack.notify_fetchrss(message)

        m_notify.assert_called_with({
            'username': 'Jaaxman',
            'channel': '#dev_notifications',
            'attachments': [{
                'title': 'job (fetchrss)',
                'text': 'TEST MESSAGE',
                'color': 'good',
                'mrkdwn_in': ['text', 'pretext'],
            }],
        })
