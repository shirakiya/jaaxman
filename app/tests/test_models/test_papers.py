from unittest.mock import patch
from app.tests.base_testcase import BaseTestCase


class PaperTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject = self.creation.rss_fetch_subject()
        self.rss_fetch_history = self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject.id,
        )

    def test_set_subject(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='Paper title. (arXiv:1708.00000 [cs.AI])',
        )
        paper._set_subject()

        self.assertEqual(paper.subject, 'cs.AI')

    def test_set_subject_updated(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='Paper title. (arXiv:1708.00000 [cs.AI] UPDATED)',
        )
        paper._set_subject()

        self.assertEqual(paper.subject, 'cs.AI')

    @patch('app.lib.google_translator.GoogleTranslator.translate')
    def test_set_translation(self, m_translate):
        m_translate.return_value = ['タイトル', '要約']

        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='TITLE',
            abstract='ABSTRACT',
        )
        paper._set_translation()

        m_translate.assert_called_with(['TITLE', 'ABSTRACT'])
        self.assertEqual(paper.title_ja, 'タイトル')
        self.assertEqual(paper.abstract_ja, '要約')

    def test_add_authors_when_given_empty_list(self):
        authors_from_xml = []
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        result = paper.add_authors(authors_from_xml)

        self.assertFalse(result)

    def test_add_authors(self):
        authors_from_xml = [
            {
                'name': 'AUTHOR_NAME_0',
                'link': 'AUTHOR_LINK_0',
            },
            {
                'name': 'AUTHOR_NAME_1',
                'link': 'AUTHOR_LINK_1',
            },
        ]
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        result = paper.add_authors(authors_from_xml)
        authors = paper.authors.all()

        self.assertTrue(result)
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].name, 'AUTHOR_NAME_0')
        self.assertEqual(authors[0].link, 'AUTHOR_LINK_0')
        self.assertEqual(authors[1].name, 'AUTHOR_NAME_1')
        self.assertEqual(authors[1].link, 'AUTHOR_LINK_1')
