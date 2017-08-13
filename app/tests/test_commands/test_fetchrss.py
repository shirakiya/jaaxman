from unittest.mock import patch
from django.core.management import call_command
from django.utils.six import StringIO
from app.tests.base_testcase import BaseTestCase
from app.models import Paper


class FetchRssTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject_0 = self.creation.rss_fetch_subject(name='NAME_0')
        self.rss_fetch_subject_1 = self.creation.rss_fetch_subject(name='NAME_1')

    @patch('app.lib.rss.arxiv.ArxivRss.fetch_and_save')
    def test_handle(self, m):
        m.return_value = [Paper(), Paper()]
        out = StringIO()
        call_command('fetchrss', stdout=out)

        self.assertIn('4 papers', out.getvalue())
