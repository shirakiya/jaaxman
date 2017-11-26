from unittest.mock import patch
from django.core.management import call_command
from app.tests.base_testcase import BaseTestCase
from app.models import RssFetchSubject


class RegisterRssTestCase(BaseTestCase):

    @patch('app.management.commands.registerrss.logger')
    def test_handle_when_rss_fetch_subjects_are_empty(self, m_logger):
        call_command('registerrss')
        rss_fetch_subjects = RssFetchSubject.objects.all()

        self.assertEqual(len(rss_fetch_subjects), 2)
        self.assertEqual(rss_fetch_subjects[0].name, 'stat.ML')
        self.assertEqual(rss_fetch_subjects[1].name, 'cs.AI')
        m_logger.info.assert_called()

    @patch('app.management.commands.registerrss.logger')
    def test_handle_when_rss_fetch_subjects_are_exists(self, m_logger):
        self.creation.rss_fetch_subject(name='stat.ML')
        call_command('registerrss')
        rss_fetch_subjects = RssFetchSubject.objects.all()

        self.assertEqual(len(rss_fetch_subjects), 2)
        self.assertEqual(rss_fetch_subjects[0].name, 'stat.ML')
        self.assertEqual(rss_fetch_subjects[1].name, 'cs.AI')
        m_logger.info.assert_called()
