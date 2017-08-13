from django.core.management import call_command
from django.utils.six import StringIO
from app.tests.base_testcase import BaseTestCase
from app.models import RssFetchSubject


class RegisterRssTestCase(BaseTestCase):

    def test_handle_when_rss_fetch_subjects_are_empty(self):
        out = StringIO()
        call_command('registerrss', stdout=out)
        rss_fetch_subjects = RssFetchSubject.objects.all()

        self.assertEqual(len(rss_fetch_subjects), 2)
        self.assertEqual(rss_fetch_subjects[0].name, 'stat.ML')
        self.assertEqual(rss_fetch_subjects[1].name, 'cs.AI')

    def test_handle_when_rss_fetch_subjects_are_exists(self):
        out = StringIO()
        self.creation.rss_fetch_subject(name='stat.ML')
        call_command('registerrss', stdout=out)
        rss_fetch_subjects = RssFetchSubject.objects.all()

        self.assertEqual(len(rss_fetch_subjects), 2)
        self.assertEqual(rss_fetch_subjects[0].name, 'stat.ML')
        self.assertEqual(rss_fetch_subjects[1].name, 'cs.AI')
