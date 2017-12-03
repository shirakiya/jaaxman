from unittest.mock import Mock
from app.tests.base_testcase import BaseTestCase
from app.lib.slack import Slack


class SlackTestCase(BaseTestCase):

    def test_notify(self):
        slack = Slack('TEST_URL')
        slack.slackweb.notify = Mock()
        payload = {
            'username': 'USERNAME',
            'channel': '#CHANNEL',
        }
        slack.notify(payload)

        slack.slackweb.notify.assert_called_with(username='USERNAME', channel='#CHANNEL')
