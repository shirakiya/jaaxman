from unittest.mock import ANY
from app.tests.base_testcase import BaseTestCase
from app.models import Paper
from app.views.helpers import (
    create_jsonable_subjects,
    _format_jsonable_date_to_papers,
    create_jsonable_date_to_papers_with_offset,
    create_jsonable_date_to_papers_with_date,
    create_jsonable_submit_types,
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

    def test_format_jsonable_date_to_papers(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history_0 = self.creation.rss_fetch_history(
            rss_fetch_subject_id=rss_fetch_subject.id,
            date='2017-08-01T20:30:00-05:00',
        )
        rss_fetch_history_1 = self.creation.rss_fetch_history(
            rss_fetch_subject_id=rss_fetch_subject.id,
            date='2017-08-02T20:30:00-05:00',
        )
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_0')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_1')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_1.id, title='PAPER_TITLE_2')
        papers = Paper.objects.order_by('-id').all()

        result = _format_jsonable_date_to_papers(papers)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(result['2017-08-01']), 2)
        self.assertEqual(len(result['2017-08-02']), 1)
        self.assertEqual(result['2017-08-01'][0]['rss_fetch_subject_id'], rss_fetch_subject.id)
        self.assertEqual(result['2017-08-01'][0]['title'], 'PAPER_TITLE_1')
        self.assertEqual(result['2017-08-01'][1]['title'], 'PAPER_TITLE_0')
        self.assertEqual(result['2017-08-02'][0]['title'], 'PAPER_TITLE_2')

    def test_create_jsonable_date_to_papers_with_offset(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)

        for i in range(100):
            self.creation.paper(
                rss_fetch_history_id=rss_fetch_history.id,
                title=f'PAPER_TITLE_{i}',
            )
        offset = 1
        result = create_jsonable_date_to_papers_with_offset(offset)

        self.assertEqual(list(result.keys()), ['2017-08-01'])
        self.assertEqual(result['2017-08-01'][0]['title'], 'PAPER_TITLE_98')  # offset分1つ少ない
        self.assertEqual(result['2017-08-01'][-1]['title'], 'PAPER_TITLE_0')
        self.assertEqual(result['2017-08-01'][0]['rss_fetch_subject_id'], rss_fetch_subject.id)
        self.assertEqual(result['2017-08-01'][-1]['rss_fetch_subject_id'], rss_fetch_subject.id)

    def test_create_jsonable_date_to_papers_with_date(self):
        rss_fetch_subject_0 = self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_0')
        rss_fetch_subject_1 = self.creation.rss_fetch_subject(name='RSS_FETCH_SUBJECT_NAME_1')
        rss_fetch_history_0 = self.creation.rss_fetch_history(
            rss_fetch_subject_id=rss_fetch_subject_0.id,
            date='2017-08-01T20:30:00-05:00',
        )
        rss_fetch_history_1 = self.creation.rss_fetch_history(
            rss_fetch_subject_id=rss_fetch_subject_0.id,
            date='2017-08-02T20:30:00-05:00',
        )
        rss_fetch_history_2 = self.creation.rss_fetch_history(
            rss_fetch_subject_id=rss_fetch_subject_1.id,
            date='2017-08-02T20:30:00-05:00',
        )
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_0')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_0.id, title='PAPER_TITLE_1')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_1.id, title='PAPER_TITLE_2')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_1.id, title='PAPER_TITLE_3')
        self.creation.paper(rss_fetch_history_id=rss_fetch_history_2.id, title='PAPER_TITLE_4')

        result = create_jsonable_date_to_papers_with_date('2017-08-02')

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['2017-08-02']), 3)
        self.assertEqual(result['2017-08-02'][0]['title'], 'PAPER_TITLE_4')
        self.assertEqual(result['2017-08-02'][1]['title'], 'PAPER_TITLE_3')
        self.assertEqual(result['2017-08-02'][2]['title'], 'PAPER_TITLE_2')

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
            {
                'name': Paper.SUBMIT_TYPE_CROSS_LISTED,
                'display_name': 'CROSS LISTED',
            },
        ])
