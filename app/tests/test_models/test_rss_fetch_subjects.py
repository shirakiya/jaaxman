import datetime

from app.tests.base_testcase import BaseTestCase


class RssFetchSubjectTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject = self.creation.rss_fetch_subject()

    def test_dumps(self):
        result = self.rss_fetch_subject.dumps()

        self.assertIsInstance(result['id'], int)
        self.assertEqual(result['name'], 'RSS_FETCH_SUBJECT_NAME')
        self.assertEqual(result['url'], 'http://example.com/')
        self.assertIsInstance(result['created_at'], datetime.datetime)
        self.assertIsInstance(result['updated_at'], datetime.datetime)
