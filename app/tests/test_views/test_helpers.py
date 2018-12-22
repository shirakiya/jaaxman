from datetime import datetime
from unittest.mock import ANY

import pytz
from freezegun import freeze_time

from app.models import Paper
from app.tests.base_testcase import BaseTestCase
from app.views.helpers import (
    _get_search_datetime_as_range,
    create_jsonable_subjects,
    create_jsonable_submit_types,
    fetch_papers_with_date,
    fetch_papers_with_offset,
    fetch_papers_with_query,
    filter_papers_with_query,
    format_jsonable_date_to_papers
)


class ViewHelperTestCase(BaseTestCase):

    def test_create_jsonable_subjects(self):
        self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_0')
        self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_1')
        result = create_jsonable_subjects()

        self.assertEqual(result, [
            {
                'id': ANY,
                'name': 'RSS_FETCH_SUBJECT_NAME_0',
                'url': 'http://example.com/',
                'created_at': ANY,
                'updated_at': ANY,
            },
            {
                'id': ANY,
                'name': 'RSS_FETCH_SUBJECT_NAME_1',
                'url': 'http://example.com/',
                'created_at': ANY,
                'updated_at': ANY,
            },
        ])

    def test_create_jsonable_submit_types(self):
        result = create_jsonable_submit_types()

        self.assertEqual(result, [
            {
                'name': Paper.SUBMIT_TYPE_NEW,
                'display_name': 'NEW',
            },
            {
                'name': Paper.SUBMIT_TYPE_UPDATED,
                'display_name': 'UPDATED',
            },
        ])

    def test_filter_papers_with_query_only_en(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)
        papers = [
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='hoge'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='fuga'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='hogefugapiyo'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title_ja='hoge fuga'),
        ]

        query = 'hoge fuga'

        result = filter_papers_with_query(papers, query)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'hogefugapiyo')

    def test_filter_papers_with_query_only_ja(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)
        papers = [
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title_ja='ほげ'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title_ja='ふが'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title_ja='ほげふがぴよ'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='ほげ ふが'),
        ]

        query = 'ほげ　ふが'

        result = filter_papers_with_query(papers, query)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title_ja, 'ほげふがぴよ')

    def test_filter_papers_with_query_in_complex_lang(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)
        papers = [
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='hoge', title_ja='ほげ'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='hoge', title_ja='ふが'),
            self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='fuga', title_ja='ほげ'),
        ]

        query = 'hoge ほげ'

        result = filter_papers_with_query(papers, query)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, 'hoge')
        self.assertEqual(result[0].title_ja, 'ほげ')

    def test_format_jsonable_date_to_papers(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)
        paper_0 = self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='PAPER_TITLE_0')
        paper_0.created_at = datetime(2017, 8, 1, 21, 0, 1)
        paper_1 = self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='PAPER_TITLE_1')
        paper_1.created_at = datetime(2017, 8, 1, 21, 0, 1)
        paper_2 = self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='PAPER_TITLE_2')
        paper_2.created_at = datetime(2017, 8, 2, 21, 0, 1)
        papers = [
            paper_2,
            paper_1,
            paper_0,
        ]

        result = format_jsonable_date_to_papers(papers)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result['2017-08-02']), 2)
        self.assertEqual(len(result['2017-08-03']), 1)
        self.assertEqual(result['2017-08-02'][0]['rss_fetch_subject_id'], rss_fetch_subject.id)
        self.assertEqual(result['2017-08-02'][0]['title'], 'PAPER_TITLE_0')
        self.assertEqual(result['2017-08-02'][1]['title'], 'PAPER_TITLE_1')
        self.assertEqual(result['2017-08-03'][0]['title'], 'PAPER_TITLE_2')

    def test_get_search_datetime_as_range(self):
        result = _get_search_datetime_as_range('2017-12-01')
        jst = pytz.timezone('Asia/Tokyo')
        expected_start_dt = datetime(2017, 11, 30, 21)
        expected_start_dt = jst.localize(expected_start_dt)
        expected_end_dt = datetime(2017, 12, 1, 21)
        expected_end_dt = jst.localize(expected_end_dt)

        self.assertEqual(result, (expected_start_dt, expected_end_dt))

    @freeze_time('2017-12-01 21:00:00')
    def test_fetch_papers_with_offset(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)

        for i in range(100):
            self.creation.paper(
                rss_fetch_history_id=rss_fetch_history.id,
                title=f'PAPER_TITLE_{i}',
            )
        offset = 1
        papers = fetch_papers_with_offset(offset)

        self.assertEqual(len(papers), 99)
        self.assertEqual(papers[0].title, 'PAPER_TITLE_98')  # less of offset

        papers = [paper for paper in papers]
        self.assertEqual(papers[-1].title, 'PAPER_TITLE_0')

    @freeze_time('2017-08-01 21:00:00')
    def test_fetch_papers_with_date(self):
        rss_fetch_subject_0 = self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_0')
        rss_fetch_subject_1 = self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_1')
        rss_fetch_history_0 = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject_0.id)
        rss_fetch_history_1 = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject_1.id)
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_0')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_1')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_1.id, title='PAPER_TITLE_2')

        papers = fetch_papers_with_date('2017-08-02')

        self.assertEqual(len(papers), 3)
        self.assertEqual(papers[0].title, 'PAPER_TITLE_2')
        self.assertEqual(papers[1].title, 'PAPER_TITLE_1')
        self.assertEqual(papers[2].title, 'PAPER_TITLE_0')

    def test_fetch_papers_with_query(self):
        rss_fetch_subject = self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_0')
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)
        self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='aaahoge', title_ja='んほげ')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='aaafuga', title_ja='んほげ')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history.id, title='aaahoge', title_ja='んふが')

        papers = fetch_papers_with_query('hoge　ほげ')

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].title, 'aaahoge')
        self.assertEqual(papers[0].title_ja, 'んほげ')
