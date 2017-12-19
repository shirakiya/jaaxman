from unittest.mock import ANY
from app.tests.base_testcase import BaseTestCase
from app.models import Paper
from app.views.helpers import (
    create_jsonable_subjects,
    create_jsonable_papers,
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

    def test_create_jsonable_papers(self):
        rss_fetch_subject = self.creation.rss_fetch_subject()
        rss_fetch_history = self.creation.rss_fetch_history(rss_fetch_subject_id=rss_fetch_subject.id)

        for i in range(100):
            self.creation.paper(
                rss_fetch_history_id=rss_fetch_history.id,
                title=f'PAPER_TITLE_{i}',
            )
        offset = 1
        result = create_jsonable_papers(offset)

        self.assertEqual(result[0]['title'], 'PAPER_TITLE_98')  # offset分1つ少ない
        self.assertEqual(result[-1]['title'], 'PAPER_TITLE_0')
        self.assertEqual(result[0]['rss_fetch_subject_id'], rss_fetch_subject.id)
        self.assertEqual(result[-1]['rss_fetch_subject_id'], rss_fetch_subject.id)

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
