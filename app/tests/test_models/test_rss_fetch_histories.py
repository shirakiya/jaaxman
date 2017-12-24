from datetime import datetime
from app.tests.base_testcase import BaseTestCase
from app.models import RssFetchHistory


class RssFetchHistoryTestCase(BaseTestCase):

    def setUp(self):
        self.test_date_0 = '2017-08-01T20:30:00-05:00'
        self.test_date_1 = '2017-08-02T20:30:00-05:00'
        self.test_date_2 = '2017-08-03T20:30:00-05:00'
        self.rss_fetch_subject_0 = self.creation.rss_fetch_subject(name='NAME_0')
        self.rss_fetch_subject_1 = self.creation.rss_fetch_subject(name='NAME_1')

    def test_exists_when_empty_in_db(self):
        result = RssFetchHistory.exists(self.rss_fetch_subject_0.id, self.test_date_0)

        self.assertFalse(result)

    def test_exists_with_same_date(self):
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_0)
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_1)
        result = RssFetchHistory.exists(self.rss_fetch_subject_0.id, self.test_date_0)

        self.assertTrue(result)

    def test_exists_with_different_date(self):
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_0)
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_1)
        result = RssFetchHistory.exists(self.rss_fetch_subject_0.id, self.test_date_2)

        self.assertFalse(result)

    def test_exists_with_same_date_and_different_rfs_id(self):
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_1.id,
            date=self.test_date_0)
        result = RssFetchHistory.exists(self.rss_fetch_subject_0.id, self.test_date_0)

        self.assertFalse(result)

    def test_cut_to_datetime(self):
        rss_fetch_history = self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_0,
        )
        result = rss_fetch_history.cut_to_datetime()

        self.assertEqual(result, '2017-08-01T20:30:00')

    def test_get_fetch_datetime(self):
        rss_fetch_history = self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject_0.id,
            date=self.test_date_0,
        )
        result = rss_fetch_history.get_fetch_datetime()

        self.assertEqual(result, datetime.strptime('2017-08-01T20:30:00', '%Y-%m-%dT%H:%M:%S'))
