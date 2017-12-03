import logging
import os
from unittest.mock import patch
from django.core.management import call_command
from app.tests.base_testcase import BaseTestCase


class NofityBuildTestCase(BaseTestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    @patch('app.lib.slack.slackweb.Slack.notify')
    def test_handle(self, m_notify):
        os.environ['SLACK_URL'] = 'SLACK_URL'
        call_command('notify_build', 'FILENAME')

        m_notify.assert_called_with(
            username='Build Notification (CircleCI)',
            channel='#dev_notifications',
            icon_emoji=':circle_ci:',
            attachments=[{
                'title': 'Build Notification',
                'text': 'Build file: FILENAME',
                'color': 'good',
                'mrkdwn_in': ['text', 'pretext'],
            }]
        )

    @patch('app.lib.slack.slackweb.Slack.notify')
    def test_handle_if_not_define_env_vars(self, m_notify):
        os.environ['SLACK_URL'] = ''
        call_command('notify_build', 'FILENAME')

        m_notify.assert_not_called()
